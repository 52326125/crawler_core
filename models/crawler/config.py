from pydantic import BaseModel


class CrawlerConfig(BaseModel):
    BASE_URL: str
    CHAPTERS_QUERY_SELECTOR: str
    CONTENT_QUERY_SELECTOR: str
    BOOK_NAME_QUERY_SELECTOR: str
    COVER_BASE_URL: str
