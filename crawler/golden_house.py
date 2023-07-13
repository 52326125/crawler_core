from typing import List
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
from converter.opencc import convert_opencc
from crawler.config.golden_house import GoldenHouseConfig
from converter.models.opencc import OpenCCModel
from crawler.models import Chapter, CrawlerWebsite
from crawler.models.htmlParser import HTMLParser
from crawler import Crawler
from crawler.models import Book, ChapterLink
from crawler.retry import retry
import uuid


class GoldenHouse(Crawler):
    website = CrawlerWebsite.GOLDEN_HOUSE

    def __init__(self) -> None:
        self.config = GoldenHouseConfig

    # TODO: should throw error if excepted
    def get_book(
        self, url: str, parser: HTMLParser, opencc: OpenCCModel | None
    ) -> Book | None:
        try:
            chapters: List["ChapterLink"] = []
            response = requests.get(url)
            soup = BeautifulSoup(response.text, parser)
            matchedTags = soup.select(self.config.CHAPTERS_QUERY_SELECTOR)
            parsed_book_url = urlparse(url)

            titleTag = soup.select_one(self.config.BOOK_NAME_QUERY_SELECTOR)
            title = convert_opencc(titleTag.text, opencc) if titleTag else ""
            book_id = self.get_book_id(url)

            cover_url = self.get_cover(url)

            for tag in matchedTags:
                chapter_url = tag["href"]
                chapter_title = convert_opencc(tag.text, opencc)
                if chapter_url.startswith("/"):
                    chapter_url = (
                        parsed_book_url.scheme
                        + "://"
                        + parsed_book_url.netloc
                        + chapter_url
                    )
                chapter: ChapterLink = {"url": chapter_url, "title": chapter_title}
                chapters.append(chapter)

            book = Book(
                chapters=chapters,
                title=title,
                cover_url=cover_url,
                identifier=book_id,
            )

            return book
        except:
            return None

    @retry
    def get_chapter(
        self, url: str, parser: HTMLParser, opencc: OpenCCModel | None = None
    ) -> Chapter:
        result: str = ""
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        if response.status_code != 200:
            print(response.status_code)
            raise Exception()

        soup = BeautifulSoup(response.text, parser)
        content = soup.select(self.config.CONTENT_QUERY_SELECTOR)

        titleTag = soup.select(self.config.TITLE_QUERY_SELECTOR)[0]
        title = titleTag.get_text().strip()
        chapter_id = url.split(",")[-1]

        for p in content:
            result = result + convert_opencc(str(p).strip(), opencc)

        chapter = Chapter(identifier=chapter_id, title=title, content=result)
        return chapter

    def get_cover(self, url: str) -> str:
        book_id = self.get_book_id(url)
        return self.config.COVER_BASE_URL + book_id + ".jpg"

    def get_book_id(self, url: str) -> str:
        return url.split("/")[-1]
