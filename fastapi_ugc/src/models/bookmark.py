from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, validator

from src.models.base import Paginated


class BookMark(BaseModel):
    film_id: str
    user_id: str
    created: Optional[datetime]

    @validator('created', pre=True, always=True)
    def set_created(cls, v):  # noqa: N805
        return v or datetime.now()


class BookMarkResponse(BookMark):
    id: str


class BookMarkResponseList(Paginated):
    data: List[BookMarkResponse]
