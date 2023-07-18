from pydantic import BaseModel


class CrawlerConfig(BaseModel):
    BASE_URL: str
    # toc
    BOOK_NAME_QUERY_SELECTOR: str
    CHAPTERS_QUERY_SELECTOR: str
    COVER_BASE_URL: str
    # chapter
    CONTENT_QUERY_SELECTOR: str
    TITLE_QUERY_SELECTOR: str
    # regex
    BOOK_ID_REGEX: str
    CHAPTER_ID_REGEX: str
