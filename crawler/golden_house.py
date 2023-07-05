from typing import List
from bs4 import BeautifulSoup
import requests
from crawler.config.golden_house import GoldenHouseConfig
from models.crawler import CrawlerWebsite
from models.htmlParser import HTMLParser
from crawler import Crawler
from models.crawler import Book, Chapter
from crawler.retry import retry
import uuid


class GoldenHouse(Crawler):
    website = CrawlerWebsite.GOLDEN_HOUSE

    def __init__(self) -> None:
        self.book_identifier = str(uuid.uuid4())
        self.config = GoldenHouseConfig

    # TODO: should throw error if excepted
    def get_book(self, url: str, parser: HTMLParser) -> Book | None:
        try:
            chapters: List["Chapter"] = []
            response = requests.get(url)
            soup = BeautifulSoup(response.text, parser)
            matchedTags = soup.select(self.config.CHAPTERS_QUERY_SELECTOR)

            nameTag = soup.select_one(self.config.BOOK_NAME_QUERY_SELECTOR)
            name = nameTag.text if nameTag else ""

            cover_url = self.get_cover(url)

            for tag in matchedTags:
                chapter: Chapter = {"url": tag["href"], "title": tag.text}
                chapters.append(chapter)

            book = Book(chapters=chapters, name=name, cover_url=cover_url)

            return book
        except:
            return None

    @retry
    def get_content(self, url: str, parser: HTMLParser):
        result: str = ""

        response = requests.get(url)
        if response.status_code != 200:
            raise Exception()

        soup = BeautifulSoup(response.text, parser)
        content = soup.select(self.config.CONTENT_QUERY_SELECTOR)
        for p in content:
            result = result + str(p)

        return result

    def get_cover(self, url: str) -> str:
        book_id = url.split("/")[-1]
        return self.config.COVER_BASE_URL + book_id + ".jpg"
