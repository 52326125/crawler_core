from pydantic import BaseSettings


class Config(BaseSettings):
    STORAGE_PATH: str = ""

    class Config:
        env_file = ".env"
