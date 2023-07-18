import re
from typing import List
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
from converter.opencc import convert_opencc
from crawler.config.golden_house import golden_house_config
from converter.models.opencc import OpenCCModel
from crawler.models import Chapter, CrawlerWebsite
from crawler.models.config import CrawlerConfig
from crawler.models.htmlParser import HTMLParser
from crawler.models import Book, ChapterLink
from crawler.utils.retry import retry


class Crawler:
    website = CrawlerWebsite.GOLDEN_HOUSE

    def __init__(self, config: CrawlerConfig) -> None:
        self.config = config

    # TODO: should throw error if excepted
    def get_book(
        self, url: str, parser: HTMLParser, opencc: OpenCCModel | None
    ) -> Book | None:
        try:
            chapters: List["ChapterLink"] = []
            response = requests.get(url)
            soup = BeautifulSoup(response.text, parser)
            matchedTags = soup.select(self.config.CHAPTERS_QUERY_SELECTOR)

            titleTag = soup.select_one(self.config.BOOK_NAME_QUERY_SELECTOR)
            title = convert_opencc(titleTag.text, opencc) if titleTag else ""
            book_id = self.get_book_id(url)

            cover_url = self.get_cover(url)

            for tag in matchedTags:
                chapter_url = tag["href"]
                chapter_title = convert_opencc(tag.text, opencc)
                if chapter_url.startswith("/"):
                    chapter_url = urljoin(self.config.BASE_URL, chapter_url)

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
        chapter_id = self.get_chapter_id(url)

        for p in content:
            result = result + convert_opencc(str(p).strip(), opencc)

        chapter = Chapter(identifier=chapter_id, title=title, content=result)
        return chapter

    def get_cover(self, url: str) -> str:
        book_id = self.get_book_id(url)
        return self.config.COVER_BASE_URL + book_id + ".jpg"

    def get_book_id(self, url: str) -> str:
        result = re.search(self.config.BOOK_ID_REGEX, url)
        return result.group(1)

    def get_chapter_id(self, url: str) -> str:
        result = re.search(self.config.CHAPTER_ID_REGEX, url)
        return result.group(1)
