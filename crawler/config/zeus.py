from crawler.models.config import CrawlerConfig


zeus_config = CrawlerConfig(
    BASE_URL="http://tw.zhsxs.com/",
    CHAPTERS_QUERY_SELECTOR="#form1 > div:nth-child(2) > table:nth-child(13) > tbody > tr > td > a",
    COVER_BASE_URL="http://tw.zhsxs.com/images/zhsid/",
    BOOK_NAME_QUERY_SELECTOR="""#form1 > div:nth-child(2) > table:nth-child(6) > tbody > tr > td > h1""",
    CONTENT_QUERY_SELECTOR="""#form1 > table:nth-child(7) > tbody > tr:nth-child(1) > td > div:nth-child(7) p""",
    TITLE_QUERY_SELECTOR="h1",
    BOOK_ID_REGEX=r"/(\d+).html",
    CHAPTER_ID_REGEX=r"_(\d+).html",
)
