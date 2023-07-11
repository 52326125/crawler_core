from pydantic import BaseSettings


class Config(BaseSettings):
    STORAGE_PATH: str = ""
    CHAPTER_STORAGE_PREFIX: str = ""
    MAXIMUM_THREAD: int

    class Config:
        env_file = ".env"
