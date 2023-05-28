import asyncio

import uvicorn
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


from settings import settings
from src.api.v1 import view_progress
from src.services import kafka_storage

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


app.include_router(view_progress.router, prefix='/api/v1/view_progress', tags=['view_progress'])


@app.on_event('startup')
async def startup():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()
    producer = AIOKafkaProducer(loop=loop, bootstrap_servers=f'{settings.kafka_host}:{settings.kafka_port}')
    kafka_storage.kafka_producer = producer
    await kafka_storage.kafka_producer.start()


@app.on_event('shutdown')
async def shutdown():
    await kafka_storage.kafka_producer.stop()


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
