from pydantic import BaseModel


class EpubBase(BaseModel):
    identifier: str
