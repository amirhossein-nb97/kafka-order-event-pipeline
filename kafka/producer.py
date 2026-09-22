import json

from confluent_kafka import Producer

from core.config import settings


producer = Producer(
    {
        "bootstrap.servers": settings.kafka_bootstrap_servers
    }
)


def delivery_report(err, message):

    if err is not None:
        print(f"Message delivery failed: {err}")

    else:
        print(
            f"Message delivered to "
            f"{message.topic()} "
            f"[{message.partition()}] "
            f"offset={message.offset()}"
        )


def send_order(order: dict):

    message = json.dumps(
        order,
        default=str,
    ).encode("utf-8")

    producer.produce(
        topic=settings.kafka_topic,
        key=str(order["id"]).encode("utf-8"),
        value=message,
        callback=delivery_report,
    )

    producer.flush()