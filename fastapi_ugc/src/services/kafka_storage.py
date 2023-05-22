import asyncio
import json
from datetime import datetime

from aiokafka import AIOKafkaProducer
from kafka.errors import KafkaError

from settings import settings


class KafkaStorage:
    def __init__(self, producer):
        self.producer = producer
        self.topic = settings.kafka_topic

    async def send_message_to_topic(self, values: dict):
        message = {
            'user_id': values.get('user_id'),
            'film_id': values.get('film_id'),
            'viewed_frame': values.get('viewed_frame'),
            'message_time': str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')),
        }

        try:
            await self.producer.send(
                key=f'{message["user_id"]}:{message["film_id"]}',
                topic=self.topic,
                value=json.dumps(message),
            )
        except KafkaError:
            pass


def get_kafka_storage() -> KafkaStorage:
    try:
        loop = asyncio.new_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()
    producer = AIOKafkaProducer(loop=loop, bootstrap_servers=f'{settings.kafka_host}:{settings.kafka_port}')
    return KafkaStorage(producer)
