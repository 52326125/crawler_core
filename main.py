from concurrent.futures import ThreadPoolExecutor, Future, as_completed
import os
from typing import List, Optional, Tuple
import requests
from crawler import Crawler
from crawler.dispatcher import dispatch_crawler
from epub.utils import create_vertical_writing_style
from epub.writer import EpubWriter
from converter.models.opencc import OpenCCModel
from crawler.models import Book, Chapter, ChapterLink
from epub.models.chapter import EpubChapterProps, EpubImageProps
from epub.models.metadata import EpubDirection, EpubMetadata
from crawler.models.htmlParser import HTMLParser
from utils.common import (
    exec_with_description,
    get_bool_input,
    get_int_input,
    get_real_path,
)
from utils.config import get_config
from utils.wrapper import select_parser


config = get_config()

default_parser = HTMLParser.DEFAULT


def press_to_exit(description: Optional[str]):
    # TODO: Accomplish needed
    if description is not None:
        print(description)
    print("點擊確認鍵後退出...")
    key = input()
    if key:
        os._exit()


def select_opencc_model() -> OpenCCModel | None:
    opencc_str = ""
    opencc_len = len(OpenCCModel)
    for index, value in enumerate(OpenCCModel):
        opencc_str += f"{index})更改opencc轉換器模組：{value}\n"
    opencc_str += f"{opencc_len})不使用opencc轉換器"
    action = get_int_input(
        description=f"請問是否使用opencc轉換器對書本內容進行轉換？\n{opencc_str}", min=0, max=opencc_len
    )
    if action == opencc_len:
        return None
    else:
        return list(OpenCCModel)[action]


def get_crawler() -> Tuple[Crawler, str]:
    book_url = input("請輸入書本網址：")
    crawler = dispatch_crawler(book_url)
    if crawler is None:
        print("無法正確匹配抓取器")
        press_to_exit()
    return crawler, book_url


@select_parser(parser_key="parser")
def parse_book(
    crawler: Crawler, parser: HTMLParser, url: str, opencc: OpenCCModel | None
) -> Book:
    book = exec_with_description(
        crawler.get_book, description="獲取書本資料", url=url, parser=parser, opencc=opencc
    )
    chapter_count = len(book.chapters)
    chapter_preview = ""
    for i in range(min(chapter_count, 5)):
        chapter_preview += book.chapters[i]["title"] + "\n"
    print(f"""獲取書本資料節錄如下：\n標題：{book.title}\n章節：\n{chapter_preview}""")
    return book


@select_parser(parser_key="parser")
def select_chapter_parser(
    chapter_link: ChapterLink, crawler: Crawler, parser: HTMLParser
) -> HTMLParser:
    chapter = exec_with_description(
        crawler.get_chapter,
        url=chapter_link["url"],
        parser=parser,
        description="獲取測試章節",
    )
    print(f"獲取測試章節節錄如下：\n標題：{chapter.title}\n內容：{chapter.content[:50]}")
    return parser


def get_epub_metadata(book_title: str) -> EpubMetadata:
    input_title = input("請輸入書名：")
    direction = input("請輸入書本方向，預設為rtl：")
    author = input("請輸入本書作者：")

    return EpubMetadata(
        title=input_title or book_title,
        direction=direction or EpubDirection.RTL,
        authors=[author],
    )


def get_book_cover(url: str) -> EpubImageProps:
    response = requests.get(url)
    return EpubImageProps(file_name="cover.jpg", file=response.content, is_cover=True)


def handle_thread(
    chapter_link: ChapterLink,
    crawler: Crawler,
    parser: HTMLParser,
    opencc: OpenCCModel | None,
    index: int,
) -> Tuple[EpubChapterProps, Chapter, int]:
    chapter = exec_with_description(
        crawler.get_chapter,
        url=chapter_link["url"],
        parser=parser,
        description=f"獲取章節：{chapter_link['title']}",
        opencc=opencc,
    )
    props = EpubChapterProps(
        identifier=chapter.identifier,
        title=chapter.title,
        file_name=chapter.identifier,
    )
    return [props, chapter.content, index]


def add_getting_chapter_concurrent_task(
    book: Book,
    parser: HTMLParser,
    crawler: Crawler,
    opencc: OpenCCModel | None,
):
    with ThreadPoolExecutor(max_workers=config.MAXIMUM_THREAD) as executor:
        futures: List[Future] = []
        result: List[Tuple[EpubChapterProps, str, int]] = []
        for index, chapter in enumerate(book.chapters):
            futures.append(
                executor.submit(
                    handle_thread,
                    chapter,
                    crawler,
                    parser=parser,
                    opencc=opencc,
                    index=index,
                )
            )

        for future in as_completed(futures):
            response = future.result()
            result.append(response)

    result.sort(key=lambda el: el[2])
    return result


def select_is_vertical_output(epub: EpubWriter, direction: EpubDirection):
    is_vertical = get_bool_input("是否轉換為直書？(Y/N)", acceptance_key=["Y", "y"])
    if not is_vertical:
        return
    epub.add_global_style(create_vertical_writing_style(direction))


if __name__ == "__main__":
    # TODO: Add keyword converter
    current_opencc = select_opencc_model()
    crawler, book_url = get_crawler()
    book: Book = parse_book(crawler=crawler, url=book_url, opencc=current_opencc)

    chapter_parser = select_chapter_parser(
        chapter_link=book.chapters[0], crawler=crawler
    )

    metadata = get_epub_metadata(book.title)
    epub = EpubWriter(metadata)

    coverProps = get_book_cover(book.cover_url)
    epub.add_image(coverProps)

    output_path = get_real_path(os.path.join(config.STORAGE_PATH, crawler.website))
    os.makedirs(output_path, exist_ok=True)
    output_file_name = f"{book.identifier}.epub"

    chapter_data = add_getting_chapter_concurrent_task(
        book=book,
        parser=chapter_parser,
        crawler=crawler,
        opencc=current_opencc,
    )
    for chapter in chapter_data:
        epub.add_chapter(props=chapter[0], content=chapter[1])

    select_is_vertical_output(epub, metadata.direction)
    epub.build(os.path.join(output_path, output_file_name))
    press_to_exit("EPUB製作完成")
