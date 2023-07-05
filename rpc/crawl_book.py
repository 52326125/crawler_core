import os
from models.rpc.message import MessageBody
from rpc.utils import new_crawler_instance
from utils.config import get_config


def crawl_book(body: MessageBody):
    config = get_config()

    crawler, payload = new_crawler_instance(body)
    book = crawler.get_book(payload.url, payload.parser)
    if book is None:
        raise Exception()

    path = os.path.join(config.STORAGE_PATH, crawler.website, crawler.book_identifier)
    os.makedirs(path)
    return book
