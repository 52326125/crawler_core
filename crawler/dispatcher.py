from crawler.golden_house import GoldenHouse
from crawler import Crawler
from crawler.config.golden_house import golden_house_config
from crawler.config.zeus import zeus_config
from crawler.zeus import Zeus


def dispatch_crawler(url: str) -> Crawler | None:
    if golden_house_config.BASE_URL in url:
        return GoldenHouse()

    if zeus_config.BASE_URL in url:
        return Zeus()

    return None
