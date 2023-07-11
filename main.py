from concurrent.futures import ThreadPoolExecutor, Future, as_completed
import os
import sys
from typing import Tuple
from crawler import Crawler
from crawler.dispatcher import dispatch_crawler
from crawler.golden_house import GoldenHouse
from epub.writer import EpubWriter
from models.crawler import Book, Chapter, ChapterLink
from models.epub.chapter import EpubChapterProps
from models.epub.metadata import EpubMetadata
from models.htmlParser import HTMLParser
from utils.common import exec_with_description, get_int_input
from utils.config import get_config
from utils.wrapper import select_parser


config = get_config()

default_parser = HTMLParser.DEFAULT


def press_to_exit():
    # TODO: Accomplish needed
    print("點擊任意鍵後退出...")
    key = input()
    if key:
        os._exit()


@select_parser(parser_key="parser")
def parse_book(crawler: Crawler, parser: HTMLParser) -> Book:
    book = exec_with_description(
        crawler.get_book, description="獲取書本資料", url=book_url, parser=parser
    )
    chapter_count = len(book.chapters)
    chapter_preview = ""
    for i in range(min(chapter_count, 10)):
        chapter_preview += book.chapters[i]["title"] + "\n"
    print(f"""獲取書本資料節錄如下：\n標題：{book.title}\n章節：{chapter_preview}""")
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


def handle_thread(
    chapter_link: ChapterLink, crawler: Crawler, parser: HTMLParser
) -> Tuple[EpubChapterProps, Chapter]:
    chapter = exec_with_description(
        crawler.get_chapter,
        url=chapter_link["url"],
        parser=parser,
        description=f"獲取章節：{chapter_link['title']}",
    )
    props = EpubChapterProps(
        identifier=chapter.identifier,
        title=chapter.title,
        file_name=f"{chapter.identifier}.xhtml",
    )
    return [props, chapter.content]


def handle_thread_done(future: Future, epub: EpubWriter):
    props, content = future.result()
    epub.add_chapter(props, content)


if __name__ == "__main__":
    book_url = input("請輸入書本網址：")
    crawler = dispatch_crawler(book_url)
    if crawler is None:
        print("無法正確匹配抓取器")
        press_to_exit()

    book = parse_book(crawler)
    chapter_parser = select_chapter_parser(
        chapter_link=book.chapters[0], crawler=crawler
    )

    output_path = os.path.join(config.STORAGE_PATH, crawler.website)
    os.makedirs(output_path, exist_ok=True)
    output_file_name = f"{book.identifier}.epub"
    metadata = EpubMetadata(title=book.title, identifier=book.identifier)
    epub = EpubWriter(metadata)

    with ThreadPoolExecutor(max_workers=config.MAXIMUM_THREAD) as executor:
        futures = []
        for index, chapter in enumerate(book.chapters):
            # if index >= 5:
            #     break
            futures.append(
                executor.submit(handle_thread, chapter, crawler, parser=chapter_parser)
            )

        for future in as_completed(futures):
            future.add_done_callback(lambda future: handle_thread_done(future, epub))

    epub.build(os.path.join(output_path, output_file_name))
