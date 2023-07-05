from pydantic import BaseModel

from models.htmlParser import HTMLParser


class CrawlerPayload(BaseModel):
    url: str
    parser: HTMLParser


class BuilderPayload(BaseModel):
    title: str
    folder_path: str
