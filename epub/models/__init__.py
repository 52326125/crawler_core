from pydantic import BaseModel, Field

from utils.uuid import get_str_uuid


class EpubBase(BaseModel):
    identifier: str = Field(default_factory=get_str_uuid)
