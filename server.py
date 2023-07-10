import asyncio
import logging

from aio_pika import Message, connect
from aio_pika.abc import AbstractIncomingMessage
from models.rpc.message import CmdEnum, MessageBody
from rpc.dispatcher import Dispatcher
from utils.config import get_config

from utils.json import str_2_pydantic


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
                    dispatcher = Dispatcher()

                    if body.cmd == CmdEnum.CRAWL_BOOK:
                        response = dispatcher.crawl_book(body)
                    elif body.cmd == CmdEnum.CRAWL_CHAPTER:
                        response = dispatcher.crawl_chapter(body)
                    elif body.cmd == CmdEnum.EPUB_BUILD:
                        dispatcher.build_book(body)

                    await exchange.publish(
                        Message(
                            body=response.json(ensure_ascii=False).encode(),
                            correlation_id=message.correlation_id,
                        ),
                        routing_key=message.reply_to,
                    )
                    print("Request complete")
            except Exception:
                logging.exception("Processing error for message %r", message)


if __name__ == "__main__":
    asyncio.run(main())
