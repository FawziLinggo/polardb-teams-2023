import asyncio
import os
import signal
from asyncio import get_event_loop, Future
from functools import partial
import websockets
from confluent_kafka import Consumer
import socket

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print(IPAddr)

bootstrap_servers = os.environ.get('BOOTSTRAP_SERVERS')
if bootstrap_servers is None:
    bootstrap_servers = '172.18.46.121:9092'

topic = os.environ.get('TOPIC')
if topic is None:
    topic = 'TradingSystemOrderProduction'

port_ws = os.environ.get('PORT_WS')
if port_ws is None:
    port_ws = 8765


c = Consumer({
    'bootstrap.servers': bootstrap_servers,
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
    c.subscribe([topic])
    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        elif msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue
        else:
            message = msg.value().decode('utf-8')
            websockets.broadcast(clients, message)

    print("Consumer Ended")
    c.close()
async def handle_connection(clients, websocket, path):
    clients.add(websocket)

    await Future()


async def main():
    clients = set()
    print("Consumer Started")
    get_event_loop().run_in_executor(None, run_consumer, clients)
    await websockets.serve(partial(handle_connection, clients), IPAddr, port_ws)


signal.signal(signal.SIGINT, signal.SIG_DFL)
asyncio.run(main())
