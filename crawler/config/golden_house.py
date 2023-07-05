from models.crawler.config import CrawlerConfig


GoldenHouseConfig = CrawlerConfig(
    BASE_URL="https://tw.hjwzw.com",
    CHAPTERS_QUERY_SELECTOR="#tbchapterlist td a",
    CONTENT_QUERY_SELECTOR="""td div[style="font-size: 20px; line-height: 30px; word-wrap: break-word; table-layout: fixed; word-break: break-all; width: 750px; margin: 0 auto; text-indent: 2em;"] p""",
    BOOK_NAME_QUERY_SELECTOR="""table[style="width: 960px; text-align: center;"] h1""",
    COVER_BASE_URL="https://tw.hjwzw.com/images/id/",
)
