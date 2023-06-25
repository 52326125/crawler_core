from typing import TypedDict

from pydantic import BaseModel

from models.converter.opencc import OpenCCModel


class KeywordDict(TypedDict):
    origin: str
    converted: str


class BookConverterForm(BaseModel):
    opencc: OpenCCModel
    keywords: list[KeywordDict]
