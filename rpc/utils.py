from typing import Tuple
from crawler import Crawler
from crawler.dispatcher import dispatch_crawler
from models.rpc.dispatcher_payload import CrawlerChapterPayload, CrawlerPayload
from models.rpc.message import CmdEnum, MessageBody
from utils.json import json_2_pydantic


def new_crawler_instance(
    body: MessageBody,
) -> Tuple[Crawler | None, CrawlerPayload | CrawlerChapterPayload]:
    payload = json_2_pydantic(
        body.payload,
        CrawlerPayload if body.cmd == CmdEnum.CRAWL_BOOK else CrawlerChapterPayload,
    )
    crawler = dispatch_crawler(payload.url)
    return crawler, payload
