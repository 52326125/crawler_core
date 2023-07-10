import asyncio
from time import sleep
import uuid
from typing import MutableMapping

from aio_pika import Message, connect
from aio_pika.abc import (
    AbstractChannel,
    AbstractConnection,
    AbstractIncomingMessage,
    AbstractQueue,
)

from models.crawler import Book


class FibonacciRpcClient:
    connection: AbstractConnection
    channel: AbstractChannel
    callback_queue: AbstractQueue
    loop: asyncio.AbstractEventLoop

    def __init__(self) -> None:
        self.futures: MutableMapping[str, asyncio.Future] = {}
        self.loop = asyncio.get_running_loop()

    async def connect(self) -> "FibonacciRpcClient":
        self.connection = await connect(
            "amqp://guest:guest@localhost/",
            loop=self.loop,
        )
        self.channel = await self.connection.channel()
        self.callback_queue = await self.channel.declare_queue(exclusive=True)
        await self.callback_queue.consume(self.on_response, no_ack=True)

        return self

    async def on_response(self, message: AbstractIncomingMessage) -> None:
        if message.correlation_id is None:
            print(f"Bad message {message!r}")
            return

        print(message)

        future: asyncio.Future = self.futures.pop(message.correlation_id)
        future.set_result(message.body)

    async def call(self, n: int) -> int:
        correlation_id = str(uuid.uuid4())
        future = self.loop.create_future()

        self.futures[correlation_id] = future

        await self.channel.default_exchange.publish(
            Message(
                str(n).encode(),
                content_type="text/plain",
                correlation_id=correlation_id,
                reply_to=self.callback_queue.name,
            ),
            routing_key="rpc_queue",
        )

        return await future


async def main() -> None:
    fibonacci_rpc = await FibonacciRpcClient().connect()
    print(" [x] Requesting fib(30)")
    # response: bytes = await fibonacci_rpc.call(
    #     '{"cmd":"CRAWL_BOOK","payload":{"url":"https://tw.hjwzw.com/Book/Chapter/44236","parser":"html5lib"}}'
    # )
    # decoded = response.decode("utf-8")
    # book = Book.parse_raw(decoded)
    # for chapter in book.chapters:
    #     print(
    #         '{"cmd":"CRAWL_CHAPTER","payload":{"url":"'
    #         + chapter["url"]
    #         + '","parser":"html5lib","book_id":44236}}'
    #     )
    #     await fibonacci_rpc.call(
    #         '{"cmd":"CRAWL_CHAPTER","payload":{"url":"'
    #         + chapter["url"]
    #         + '","parser":"html5lib","book_id":44236}}'
    #     )
    #     sleep(0.5)
    # sleep(1)
    # response = await fibonacci_rpc.call(
    #     '{"cmd":"CRAWL_CHAPTER","payload":{"url":"https://tw.hjwzw.com/Book/Read/1642,530186","parser":"html5lib","book_id":1642}}'
    # )
    # print(f" [.] Got {response!r}")
    # await fibonacci_rpc.call(
    #     '{"cmd":"EPUB_BUILD","payload":{"user_id":1,"book_id":44236,"name":"詭秘地海","crawler":"golden_house","options":{"opencc":"t2s.json","is_vertical":true,"cover_path":"https://tw.hjwzw.com/images/id/44236.jpg","direction":"rtl","chapters":["20286720","20286721"]}}}'
    # )


if __name__ == "__main__":
    asyncio.run(main())
