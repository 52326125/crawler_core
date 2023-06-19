from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_DRIVER: str = ""
    DB_SERVER: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_DB: str = ""

    REDIS_SERVER: str = ""
    REDIS_DB: int = 0

    TOKEN_SECRET: str = ""
    TOKEN_ALGORITHM: str = ""
    TOKEN_EXPIRE_MINUTES: int = 0
    TOKEN_REFRESH_EXPIRE_MINUTES: int = 0

    class Config:
        env_file = ".env"
