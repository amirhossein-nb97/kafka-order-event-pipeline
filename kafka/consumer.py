import json

from confluent_kafka import Consumer

from core.config import settings
from app.database.base import Base
from app.database.session import SessionLocal, engine
from app.entities.order.model import Order


Base.metadata.create_all(
    bind=engine
)


consumer = Consumer(
    {
        "bootstrap.servers": settings.kafka_bootstrap_servers,
        "group.id": settings.kafka_group_id,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
    }
)


consumer.subscribe(
    [settings.kafka_topic]
)


def save_order(order_data: dict):

    db = SessionLocal()

    try:

        existing_order = (
            db.query(Order)
            .filter(
                Order.id == order_data["id"]
            )
            .first()
        )

        if existing_order:

            print(
                f"Order {order_data['id']} "
                f"already exists"
            )

            return

        order = Order(
            id=order_data["id"],
            user_id=order_data["user_id"],
            product_id=order_data["product_id"],
            amount=order_data["amount"],
            status=order_data["status"],
        )

        db.add(order)

        db.commit()

        print(
            f"Order {order.id} "
            f"saved to PostgreSQL"
        )

    except Exception as e:

        db.rollback()

        print(
            f"Database error: {e}"
        )

        raise

    finally:

        db.close()


def consume():

    print(
        "Kafka consumer started..."
    )

    try:

        while True:

            message = consumer.poll(
                timeout=1.0
            )

            if message is None:
                continue

            if message.error():

                print(
                    f"Kafka error: "
                    f"{message.error()}"
                )

                continue

            try:

                order_data = json.loads(
                    message.value()
                    .decode("utf-8")
                )

                print(
                    f"Received: {order_data}"
                )

                save_order(
                    order_data
                )

                consumer.commit(
                    message=message
                )

            except Exception as e:

                print(
                    f"Message processing failed: "
                    f"{e}"
                )

    except KeyboardInterrupt:

        print(
            "Consumer stopped."
        )

    finally:

        consumer.close()


if __name__ == "__main__":
    consume()