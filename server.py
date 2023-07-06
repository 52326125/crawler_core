import asyncio
import logging
from typing import Tuple

from aio_pika import Message, connect
from aio_pika.abc import AbstractIncomingMessage
from crawler import Crawler
from crawler.dispatcher import dispatch_crawler
from models.rpc.dispatcher_payload import CrawlerPayload
from models.rpc.message import CmdEnum, MessageBody
from rpc.crawl_chapter import crawl_chapter
from rpc.crawl_book import crawl_book
from utils.config import get_config

from utils.json import json_2_pydantic, str_2_pydantic


config = get_config()
print(config.STORAGE_PATH)


async def main() -> None:
    # Perform connection
    connection = await connect("amqp://guest:guest@localhost/")

    # Creating a channel
    channel = await connection.channel()
    exchange = channel.default_exchange

    # Declaring queue
    queue = await channel.declare_queue("rpc_queue")

    print(" [x] Awaiting RPC requests")

    # Start listening the queue
    async with queue.iterator() as qiterator:
        message: AbstractIncomingMessage
        async for message in qiterator:
            try:
                async with message.process(requeue=False):
                    assert message.reply_to is not None

                    body_str = message.body.decode()
                    body = str_2_pydantic(body_str, MessageBody)

                    if body.cmd == CmdEnum.CRAWL_BOOK:
                        response = crawl_book(body)
                    elif body.cmd == CmdEnum.CRAWL_CHAPTER:
                        # done
                        response = crawl_chapter(body)
                    elif body.cmd == CmdEnum.EPUB_BUILD:
                        print("3")

                    await exchange.publish(
                        Message(
                            body=str(response).encode(),
                            correlation_id=message.correlation_id,
                        ),
                        routing_key=message.reply_to,
                    )
                    print("Request complete")
            except Exception:
                logging.exception("Processing error for message %r", message)


if __name__ == "__main__":
    asyncio.run(main())
