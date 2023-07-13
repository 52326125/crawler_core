from datetime import datetime
from typing import List, TypedDict
from enum import Enum
from pydantic import BaseModel


class CrawlerWebsite(str, Enum):
    GOLDEN_HOUSE = "golden_house"


class BaseInstance(BaseModel):
    identifier: str


class ChapterLink(TypedDict):
    url: str | List[str]
    title: str


class Book(BaseInstance):
    title: str
    chapters: List[ChapterLink]
    updated_at: datetime = datetime.today()
    cover_url: str


class Chapter(BaseInstance):
    title: str
    content: str
