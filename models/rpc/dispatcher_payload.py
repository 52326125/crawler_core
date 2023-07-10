from typing import Dict, List, Optional
from pydantic import BaseModel
from models.converter.opencc import OpenCCModel
from models.crawler import CrawlerWebsite
from models.epub.metadata import EpubDirection

from models.htmlParser import HTMLParser


class CrawlerPayload(BaseModel):
    url: str
    parser: HTMLParser


class CrawlerChapterPayload(CrawlerPayload):
    book_id: str


class BuilderPayloadOptions(BaseModel):
    opencc: OpenCCModel
    is_vertical: bool = False
    keywords: Optional[Dict[str, str]] = None
    cover_path: str
    is_customize_cover: bool = False
    direction: EpubDirection
    chapters: List[str]


class BuilderPayload(BaseModel):
    user_id: str
    book_id: str
    name: str
    crawler: CrawlerWebsite
    options: BuilderPayloadOptions
