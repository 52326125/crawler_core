from crawler import Crawler
from crawler.config.golden_house import golden_house_config
from crawler.config.zeus import zeus_config


def dispatch_crawler(url: str) -> Crawler | None:
    if golden_house_config.BASE_URL in url:
        return Crawler(golden_house_config)

    if zeus_config.BASE_URL in url:
        return Crawler(zeus_config)

    return None
