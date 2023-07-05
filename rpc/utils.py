from typing import Tuple
from crawler import Crawler
from crawler.dispatcher import dispatch_crawler
from models.rpc.dispatcher_payload import CrawlerPayload
from models.rpc.message import MessageBody
from utils.json import json_2_pydantic


def new_crawler_instance(body: MessageBody) -> Tuple[Crawler | None, CrawlerPayload]:
    payload = json_2_pydantic(body.payload, CrawlerPayload)
    crawler = dispatch_crawler(payload.url)
    return crawler, payload
