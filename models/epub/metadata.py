from enum import Enum
from typing import Optional

from models.epub import EpubBase


class EpubDirection(str, Enum):
    LTR = "ltr"
    RTL = "rtl"


class EpubMetadata(EpubBase):
    title: str
    language: str = "zh-TW"
    authors: Optional[list[str]]
    direction: EpubDirection = EpubDirection.LTR
