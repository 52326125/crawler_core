from functools import lru_cache

from models.config import Config


@lru_cache
def get_config() -> Config:
    return Config()
