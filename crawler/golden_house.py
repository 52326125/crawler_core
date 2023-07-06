from typing import List
from bs4 import BeautifulSoup
import requests
from crawler.config.golden_house import GoldenHouseConfig
from models.crawler import Chapter, CrawlerWebsite
from models.htmlParser import HTMLParser
from crawler import Crawler
from models.crawler import Book, ChapterLink
from crawler.retry import retry
import uuid


class GoldenHouse(Crawler):
    website = CrawlerWebsite.GOLDEN_HOUSE

    def __init__(self) -> None:
        self.config = GoldenHouseConfig

    # TODO: should throw error if excepted
    def get_book(self, url: str, parser: HTMLParser) -> Book | None:
        try:
            chapters: List["ChapterLink"] = []
            response = requests.get(url)
            soup = BeautifulSoup(response.text, parser)
            matchedTags = soup.select(self.config.CHAPTERS_QUERY_SELECTOR)

            titleTag = soup.select_one(self.config.BOOK_NAME_QUERY_SELECTOR)
            title = titleTag.text if titleTag else ""
            book_id = self.get_book_id(url)

            cover_url = self.get_cover(url)

            for tag in matchedTags:
                chapter: ChapterLink = {"url": tag["href"], "title": tag.text}
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
    def get_chapter(self, url: str, parser: HTMLParser) -> Chapter:
        result: str = ""

        response = requests.get(url)
        print(response)
        if response.status_code != 200:
            print(response.status_code)
            raise Exception()

        soup = BeautifulSoup(response.text, parser)
        content = soup.select(self.config.CONTENT_QUERY_SELECTOR)
        title = soup.select(self.config.TITLE_QUERY_SELECTOR)
        chapter_id = url.split(",")[-1]
        # TODO: find error
        for p in content:
            result = result + str(p)

        chapter = Chapter(identifier=chapter_id, title=title, content=result)
        return chapter

    def get_cover(self, url: str) -> str:
        book_id = self.get_book_id(url)
        return self.config.COVER_BASE_URL + book_id + ".jpg"

    def get_book_id(self, url: str) -> str:
        return url.split("/")[-1]
