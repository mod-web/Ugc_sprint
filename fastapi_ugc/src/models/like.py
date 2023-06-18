from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, validator

from src.models.base import Paginated


class Like(BaseModel):
    film_id: str
    user_id: str
    rate: int


class FilmRate(BaseModel):
    film_id: str
    average_rate: float
