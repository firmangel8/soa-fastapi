from confluent_kafka import Consumer, KafkaException
import os, dotenv
from msgpack import unpackb
from helper.payload import deconstruct_payload
import signal

dotenv.load_dotenv()

TOPIC_NAME = os.getenv("TOPIC_NAME")
KAFKA_NETWORK = os.getenv("KAFKA_NETWORK")

running = True

def shutdown(sig, frame):
    global running
    print("\nShutting down consumer...")
    running = False

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

def process_message(msg):
    message_unpack = unpackb(msg.value(), raw=False)
    topic, message, sender = deconstruct_payload(message_unpack)
    print({"topic": topic, "message": message, "sender": sender})

consumer = Consumer({
    "bootstrap.servers": KAFKA_NETWORK,
    "group.id": "trpl-group-id-event-stream-trpl",
    "auto.offset.reset": "earliest"
})

consumer.subscribe([TOPIC_NAME])

try:
    while running:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            print("Consumer error:", msg.error())
            continue

        process_message(msg)

finally:
    consumer.close()
