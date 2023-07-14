from pydantic import BaseSettings
from utils.common import get_real_path


class Config(BaseSettings):
    STORAGE_PATH: str = ""
    CHAPTER_STORAGE_PREFIX: str = ""
    MAXIMUM_THREAD: int

    class Config:
        env_file = get_real_path("config")
