from abc import ABC, abstractmethod

from models.crawler import Book, CrawlerWebsite
from models.crawler.config import CrawlerConfig
from models.htmlParser import HTMLParser


class Crawler(ABC):
    website: CrawlerWebsite
    config: CrawlerConfig
    book_identifier: str

    @abstractmethod
    def get_book(self, url: str, parser: HTMLParser) -> Book:
        pass

    @abstractmethod
    def get_content(self, url: str, parser: HTMLParser) -> str:
        pass
