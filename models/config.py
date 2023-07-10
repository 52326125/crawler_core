from pydantic import BaseSettings


class Config(BaseSettings):
    STORAGE_PATH: str = ""
    CHAPTER_STORAGE_PREFIX: str = ""

    class Config:
        env_file = ".env"
