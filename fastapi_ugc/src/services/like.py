from functools import lru_cache
from fastapi import HTTPException
from http import HTTPStatus
from settings import settings
from src.models.like import Like
from src.services.mongo_base import MongoServiceBase
from src.services.mongo_db import mongo_client


class LikeService(MongoServiceBase):

    async def create_like(self, like: Like) -> Like:
        """Создать лайк"""
        data = await self.find_one({"user_id": like.user_id, "film_id": like.film_id})
        if data:
            if like.rate == data.rate:
                return data
            await self.delete(**data)
        data = Like(user_id=like.user_id, film_id=like.film_id, rate=like.rate)
        await self.insert_one(like.dict())
        return data

    async def remove_like(self, like: Like) -> None:
        """Удалить лайк"""
        data = await self.find_one({"user_id": like.user_id, "film_id": like.film_id})
        if not data:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
        await self.delete(**data)

    async def get_film_rate(self, film_id: str) -> dict:
        """Получить рейтинг фильма"""
        data = await self.find_all(**{"film_id": film_id})
        return {'film_id': film_id, 'average_rate': sum([film_like.rate for film_like in data])/len(data)}


@lru_cache(maxsize=None)
def get_likes_service():
    client = mongo_client
    db_name = client[settings.mongodb_name]
    collection_name = db_name[settings.mongodb_collection_likes]
    return LikeService(collection_name)
