import asyncio
import signal
from asyncio import get_event_loop, Future
from functools import partial

import websockets
from confluent_kafka import Consumer

c = Consumer({
    'bootstrap.servers': '172.18.46.121:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': 'false',
    'enable.auto.offset.store': 'false',
    'session.timeout.ms': 6000,
    'default.topic.config': {'auto.offset.reset': 'beginning'}
}
)


# Subscribe to topic
def run_consumer(clients):
    c.subscribe(['TradingSystemOrder3'])
    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        elif msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue
        else:
            message = msg.value().decode('utf-8')
            print(message)
            websockets.broadcast(clients, message)

    print("Consumer Ended")
    c.close()
async def handle_connection(clients, websocket, path):
    clients.add(websocket)

    # await websocket.send("Hello World!")
    await Future()


async def main():
    clients = set()

    print("Consumer Started")
    get_event_loop().run_in_executor(None, run_consumer, clients)
    await websockets.serve(partial(handle_connection, clients), 'localhost', 8765)


signal.signal(signal.SIGINT, signal.SIG_DFL)
asyncio.run(main())
