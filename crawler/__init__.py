from abc import ABC, abstractmethod
from converter.models.opencc import OpenCCModel

from crawler.models import Book, Chapter, CrawlerWebsite
from crawler.models.config import CrawlerConfig
from crawler.models.htmlParser import HTMLParser


class Crawler(ABC):
    website: CrawlerWebsite
    config: CrawlerConfig

    @abstractmethod
    def get_book(
        self, url: str, parser: HTMLParser, opencc: OpenCCModel | None = None
    ) -> Book:
        pass

    @abstractmethod
    def get_chapter(
        self, url: str, parser: HTMLParser, opencc: OpenCCModel | None
    ) -> Chapter:
        pass

    @abstractmethod
    def get_cover(self, url: str) -> str:
        pass

    @abstractmethod
    def get_book_id(self, url: str) -> str:
        pass
