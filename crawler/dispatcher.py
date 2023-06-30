from crawler.golden_house import GoldenHouse
from crawler import Crawler
from crawler.config.golden_house import GoldenHouseConfig


def dispatch_crawler(url: str) -> Crawler | None:
    if GoldenHouseConfig.BASE_URL in url:
        return GoldenHouse()

    return None
