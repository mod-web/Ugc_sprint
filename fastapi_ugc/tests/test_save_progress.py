import json
from time import sleep

import requests
from datetime import datetime

from kafka import KafkaProducer, KafkaConsumer

from tests.conftest import HOST, PORT, USER_ID, FILM_ID, VIEWED_FRAME, KAFKA_TEST_TOPIC, KAFKA_PORT

data = {
            'user_id': USER_ID,
            'film_id': FILM_ID,
            'viewed_frame': VIEWED_FRAME,
            'message_time': str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')),
        }


def test_save_movie_progress():
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = f'http://{HOST}:{PORT}/api/v1/view_progress/save'
    response = requests.post(url=url,
                             json=data,
                             headers=headers
                             )
    assert response.status_code == 200


def test_send_event_to_topic(create_and_delete_test_topic):
    """Проверка отправки события в Kafka"""

    producer = KafkaProducer(bootstrap_servers=f'{HOST}:{KAFKA_PORT}')
    producer.send(
            key=f'{data["user_id"]}:{data["film_id"]}'.encode('utf-8'),
            topic=KAFKA_TEST_TOPIC,
            value=json.dumps(data).encode('utf-8'),
        )
    sleep(1)
    consumer = KafkaConsumer(
        KAFKA_TEST_TOPIC,
        bootstrap_servers=[f'{HOST}:{KAFKA_PORT}'],
        auto_offset_reset='earliest',
        group_id='echo-messages-to-stdout',
    )
    kafka_data = consumer.next().value
    for field_name, field_value in data.items():
        assert kafka_data[field_name] == field_value


# def test_load_message_to_clickhouse(create_and_delete_test_topic):
#     """Проверка загрузки сообщения в ClickHouse"""
#
#     producer = KafkaProducer(bootstrap_servers=f'{HOST}:{KAFKA_PORT}')
#     producer.send(
#             key=f'{data["user_id"]}:{data["film_id"]}'.encode('utf-8'),
#             topic=KAFKA_TEST_TOPIC,
#             value=json.dumps(data).encode('utf-8'),
#         )
#     sleep(1)
