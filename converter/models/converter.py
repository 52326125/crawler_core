from typing import TypedDict

from pydantic import BaseModel

from converter.models.opencc import OpenCCModel


class KeywordDict(TypedDict):
    origin: str
    converted: str


class BookConverterForm(BaseModel):
    opencc: OpenCCModel
    keywords: list[KeywordDict]
