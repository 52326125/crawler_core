from pydantic import BaseModel

from models.htmlParser import HTMLParser


class CrawlerPayload(BaseModel):
    url: str
    parser: HTMLParser
