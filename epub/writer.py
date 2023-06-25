from ebooklib.epub import (
    EpubBook,
    EpubHtml,
    EpubItem,
    EpubNcx,
    write_epub,
    EpubNav,
    EpubImage,
)
from models.epub.chapter import EpubChapterProps, EpubImageProps

from models.epub.metadata import EpubMetadata


class EpubWriter:
    def __init__(self, metadata: EpubMetadata):
        self.__book = EpubBook()
        self.__global_style: EpubItem | None = None
        self.__chapters: list[EpubHtml] = []

        self.__book.set_identifier(metadata.identifier)
        self.__book.set_language(metadata.language)
        self.__book.set_title(metadata.title)
        self.__book.set_direction(metadata.direction)

        if metadata.authors:
            for author in metadata.authors:
                self.__book.add_author(author=author)
        pass

    def add_chapter(self, props: EpubChapterProps, content: str):
        chapter = EpubHtml(
            uid=props.identifier,
            title=props.title,
            media_type="application/xhtml+xml",
            file_name=props.file_name + ".xhtml",
        )
        chapter.set_content(content)
        self.__book.add_item(chapter)
        self.__chapters.append(chapter)

    def add__global_style(self, content: str):
        if not self.__global_style:
            self.__global_style = EpubItem(
                file_name="global.css", media_type="text/css"
            )

        self.__global_style.set_content(content)
        self.__book.add_item(self.__global_style)

    def build(self, file_name: str, sort: bool = True):
        ncx = EpubNcx()
        nav = EpubNav()
        self.__book.add_item(ncx)
        self.__book.add_item(nav)

        if sort:
            self.__book.toc = sorted(
                self.__chapters, key=lambda chapter: chapter.file_name
            )
            self.__book.items.sort(key=lambda chapter: chapter.file_name)
        else:
            self.__book.toc = self.__chapters

        if self.__global_style:
            for chapter in self.__chapters:
                chapter.add_item(self.__global_style)

        self.__book.spine = [nav] + self.__chapters
        write_epub(file_name, self.__book)

    def add_image(self, props: EpubImageProps):
        image = EpubImage(
            file_name=props.file_name, content=props.file, uid=props.identifier
        )
        if props.is_cover:
            self.__book.set_cover(file_name=props.file_name, content=props.file)
        else:
            self.__book.add_item(image)
