from confluent_kafka.avro import AvroConsumer
import avro
c = AvroConsumer({
    'bootstrap.servers': '172.18.46.121:9092',
    'group.id': 'testes',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': 'false',
    'schema.registry.url': 'http://172.18.46.121:8081'})

c.subscribe(['dlq'])

while True:
    msg = c.poll(1.0)

    if msg is None:
        print("No message received by consumer")
        continue
    if msg.error():
        print("AvroConsumer error: {}".format(msg.error()))
        continue

    print(msg.value(), msg.headers())