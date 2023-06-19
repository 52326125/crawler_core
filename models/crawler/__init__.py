from datetime import datetime
from typing import List, TypedDict
from enum import Enum
from pydantic import BaseModel


class CrawlerWebsite(str, Enum):
    GOLDEN_HOUSE = "golden_house"


class Chapter(TypedDict):
    url: str | List[str]
    title: str


class Book(BaseModel):
    name: str
    chapters: List[Chapter]
    updated_at: datetime = datetime.today()
