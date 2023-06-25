from typing import List
from bs4 import BeautifulSoup
import requests
from models.crawler.golden_house import GoldenHouseConfig
from models.crawler import CrawlerWebsite
from models.htmlParser import HTMLParser
from crawler import Crawler
from models.crawler import Book, Chapter
from crawler.retry import retry


class GoldenHouse(Crawler):
    website = CrawlerWebsite.GOLDEN_HOUSE

    def __init__(self, url: str) -> None:
        self.book_url = url
        self.book_identifier = url.split("/")[-1].split(",")[0]
        self.config = GoldenHouseConfig

    def get_book(self, parser: HTMLParser) -> Book | None:
        try:
            chapters: List["Chapter"] = []
            response = requests.get(self.book_url)
            soup = BeautifulSoup(response.text, parser)
            matchedTags = soup.select(self.config.CHAPTERS_QUERY_SELECTOR)

            nameTag = soup.select_one(self.config.BOOK_NAME_QUERY_SELECTOR)
            name = nameTag.text if nameTag else ""

            for tag in matchedTags:
                chapter: Chapter = {"url": tag["href"], "title": tag.text}
                chapters.append(chapter)

            book = Book(chapters=chapters, name=name)

            return book
        except:
            return None

    @retry
    def get_content(self, url, parser):
        result: str = ""

        response = requests.get(url)
        if response.status_code != 200:
            raise Exception()

        soup = BeautifulSoup(response.text, parser)
        content = soup.select(self.config.CONTENT_QUERY_SELECTOR)
        for p in content:
            result = result + str(p)

        return result
