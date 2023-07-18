from crawler.models.config import CrawlerConfig


golden_house_config = CrawlerConfig(
    BASE_URL="https://tw.hjwzw.com",
    CHAPTERS_QUERY_SELECTOR="#tbchapterlist td a",
    COVER_BASE_URL="https://tw.hjwzw.com/images/id/",
    BOOK_NAME_QUERY_SELECTOR="""table[style="width: 960px; text-align: center;"] h1""",
    CONTENT_QUERY_SELECTOR="""td div[style="font-size: 20px; line-height: 30px; word-wrap: break-word; table-layout: fixed; word-break: break-all; width: 750px; margin: 0 auto; text-indent: 2em;"] p""",
    TITLE_QUERY_SELECTOR="h1",
    BOOK_ID_REGEX=r"/(\d+)",
    CHAPTER_ID_REGEX=r",(\d+)",
)
