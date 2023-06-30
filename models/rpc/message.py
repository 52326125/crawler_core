from enum import Enum
from pydantic import BaseModel


class CmdEnum(str, Enum):
    CRAWL_BOOK = "CRAWL_BOOK"
    CRAWL_CHAPTER = "CRAWL_CHAPTER"
    EPUB_BUILD = "EPUB_BUILD"


class MessageBody(BaseModel):
    cmd: CmdEnum
    payload: dict
