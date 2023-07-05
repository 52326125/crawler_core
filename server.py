import asyncio
import logging
from typing import Tuple

from aio_pika import Message, connect
from aio_pika.abc import AbstractIncomingMessage
from crawler import Crawler
from crawler.dispatcher import dispatch_crawler
from models.rpc.dispatcher_payload import CrawlerPayload
from models.rpc.message import CmdEnum, MessageBody

from utils.json import json_2_pydantic, str_2_pydantic


def new_crawler_instance(body: MessageBody) -> Tuple[Crawler | None, CrawlerPayload]:
    payload = json_2_pydantic(body.payload, CrawlerPayload)
    crawler = dispatch_crawler(payload.url)
    return crawler, payload


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
                    print(body_str)
                    body = str_2_pydantic(body_str, MessageBody)

                    if body.cmd == CmdEnum.CRAWL_BOOK:
                        # done
                        crawler, payload = new_crawler_instance(body)
                        response = crawler.get_book(payload.url, payload.parser)
                    elif body.cmd == CmdEnum.CRAWL_CHAPTER:
                        # done
                        crawler, payload = new_crawler_instance(body)
                        response = crawler.get_content(payload.url, payload.parser)
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
