from src.models.base import Created


class ReviewLike(Created):
    user_id: str
    review_id: str
    like: bool


class ReviewMovie(Created):
    film_id: str
    user_id: str
    text: str


class ReviewResponse(ReviewMovie):
    id: str
