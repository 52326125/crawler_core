from pydantic import BaseModel
from epub.models import EpubBase


class EpubAssets(BaseModel):
    file_name: str


class EpubChapterProps(EpubBase, EpubAssets):
    title: str


class EpubImageProps(EpubBase, EpubAssets):
    file: bytes
    is_cover: bool = False


class EpubCoverProps(EpubBase, EpubAssets):
    file: bytes
    is_cover: bool = True
