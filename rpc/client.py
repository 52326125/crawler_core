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
    for i in range(1):
        response = await fibonacci_rpc.call(
            '{"cmd":"CRAWL_BOOK","payload":{"url":"https://tw.hjwzw.com/Book/Chapter/1642","parser":"html5lib"}}'
        )
        sleep(1)
        response = await fibonacci_rpc.call(
            '{"cmd":"CRAWL_CHAPTER","payload":{"url":"https://tw.hjwzw.com/Book/Read/1642,530186","parser":"lxml","book_id":1642}}'
        )
        print(f" [.] Got {response!r}")


if __name__ == "__main__":
    asyncio.run(main())
