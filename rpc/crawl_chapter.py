import os
from models.rpc.message import MessageBody
from rpc.utils import new_crawler_instance
from utils.config import get_config


def crawl_chapter(body: MessageBody):
    config = get_config()

    crawler, payload = new_crawler_instance(body)
    chapter = crawler.get_chapter(payload.url, payload.parser)

    path = os.path.join(
        config.STORAGE_PATH,
        crawler.website,
        payload.book_id,
        f"{chapter.identifier}.json",
    )
    with open(path, "w+") as output:
        output.write(chapter.dict())
    return chapter
