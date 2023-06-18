import logging
from typing import Any, Dict, Optional

from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.errors import DuplicateKeyError

logger = logging.getLogger(__name__)


class MongoServiceBase:
    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self.collection = collection

    async def insert_one(self, data: Dict) -> Optional[Dict[str, Any]]:
        try:
            result = await self.collection.insert_one(data)
        except DuplicateKeyError:
            logger.info('duplicate key error')
            raise HTTPException(
                status_code=409,
                detail='record with the same id already exists',
            )

        inserted_id = result.inserted_id
        inserted_doc = await self.collection.find_one({'_id': inserted_id})
        logger.info('document inserted with id {0}'.format(inserted_id))
        inserted_doc_json = self.transform_to_json(inserted_doc)
        return inserted_doc_json

    def transform_to_json(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        doc['id'] = str(doc.pop('_id'))
        return doc
