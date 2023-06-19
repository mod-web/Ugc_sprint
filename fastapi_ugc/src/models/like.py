from pydantic import BaseModel


class Like(BaseModel):
    film_id: str
    user_id: str
    rate: int


class FilmRate(BaseModel):
    film_id: str
    average_rate: float
