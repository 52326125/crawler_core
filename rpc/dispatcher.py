import os

import requests
from epub.utils import create_vertical_writing_style
from epub.writer import EpubWriter
from models.config import Config
from models.crawler import Book, Chapter
from models.epub.chapter import EpubChapterProps, EpubImageProps
from models.epub.metadata import EpubDirection, EpubMetadata
from models.rpc.dispatcher_payload import BuilderPayload
from models.rpc.message import MessageBody
from rpc.utils import new_crawler_instance
from utils.json import json_2_pydantic, str_2_pydantic


class Dispatcher:
    def __init__(self):
        self.config = Config()

    def crawl_book(self, body: MessageBody) -> Book:
        crawler, payload = new_crawler_instance(body)
        book = crawler.get_book(payload.url, payload.parser)
        if book is None:
            raise Exception()

        path = os.path.join(self.config.STORAGE_PATH, crawler.website, book.identifier)
        chapter_path = os.path.join(path, self.config.CHAPTER_STORAGE_PREFIX)
        os.makedirs(path, exist_ok=True)
        os.makedirs(chapter_path, exist_ok=True)
        return book

    def crawl_chapter(self, body: MessageBody) -> Chapter:
        crawler, payload = new_crawler_instance(body)
        chapter = crawler.get_chapter(payload.url, payload.parser)

        chapter_path = os.path.join(
            self.config.STORAGE_PATH,
            crawler.website,
            payload.book_id,
            self.config.CHAPTER_STORAGE_PREFIX,
            f"{chapter.identifier}.json",
        )
        with open(chapter_path, "w") as output:
            jsonStr = chapter.json(ensure_ascii=False)
            output.write(jsonStr)
        return chapter

    def build_book(self, body: MessageBody) -> str:
        payload = json_2_pydantic(body.payload, BuilderPayload)
        output_path = os.path.join(
            self.config.STORAGE_PATH, payload.user_id, f"{payload.book_id}.epub"
        )
        book_path = os.path.join(
            self.config.STORAGE_PATH, payload.crawler, payload.book_id
        )

        # TODO: Add more options
        epub_metadata = EpubMetadata(title=payload.name, identifier=payload.book_id)
        epub = EpubWriter(epub_metadata)
        cover = None

        if payload.options.is_customize_cover:
            cover = open(payload.options.cover_path, "rb").read()
        else:
            cover = requests.get(payload.options.cover_path).content

        cover_props = EpubImageProps(file=cover, is_cover=True, file_name="cover.jpg")
        epub.add_image(cover_props)

        if payload.options.is_vertical:
            epub.add_global_style(
                create_vertical_writing_style(payload.options.direction)
            )

        for chapter in payload.options.chapters:
            chapter_file_name = f"{chapter}.json"
            chapter_file_path = os.path.join(
                book_path, self.config.CHAPTER_STORAGE_PREFIX, chapter_file_name
            )
            with open(chapter_file_path, "r") as chapter_file:
                file_content = chapter_file.read()
                chapter = str_2_pydantic(file_content, Chapter)
                chapter_props = EpubChapterProps(
                    identifier=chapter.identifier,
                    title=chapter.title,
                    file_name=f"{chapter.identifier}.xhtml",
                )
                epub.add_chapter(chapter_props, chapter.content)

        epub.build(output_path)
