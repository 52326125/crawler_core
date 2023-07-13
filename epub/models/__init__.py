from uuid import uuid4
from pydantic import BaseModel


class EpubBase(BaseModel):
    identifier: str = str(uuid4())
