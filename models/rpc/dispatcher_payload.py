from pydantic import BaseModel

from models.htmlParser import HTMLParser


class CrawlerPayload(BaseModel):
    url: str
    parser: HTMLParser


class CrawlerChapterPayload(CrawlerPayload):
    book_id: str


class BuilderPayload(BaseModel):
    title: str
    folder_path: str
