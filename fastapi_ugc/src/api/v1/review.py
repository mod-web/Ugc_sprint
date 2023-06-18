from fastapi import APIRouter, Depends, Path

from src.models.review import ReviewMovie, ReviewResponse
from src.services.review import get_reviews_service, ReviewService

router = APIRouter()


@router.post(
    '',
    description='Save review to mongo',
    summary='Save review to mongo',
    response_model=ReviewResponse,
    # dependencies=[Depends(Access({'admin', 'subscriber'}))],
)
async def save_view_review_to_mongo(
    review_data: ReviewMovie,
    review_service: ReviewService = Depends(get_reviews_service),
):
    return await review_service.insert_one(review_data.dict())


@router.post(
    '/{id}/like',
    description='Save like for review',
    summary='Save like for review',
    # response_model=ReviewResponse,
    # dependencies=[Depends(Access({'admin', 'subscriber'}))],
)
async def save_view_review_to_mongo(
    like: bool,
    review_service: ReviewService = Depends(get_reviews_service),
    id_: str = Path(alias='id'),
):
    return await review_service.patch_one(id_, like)
