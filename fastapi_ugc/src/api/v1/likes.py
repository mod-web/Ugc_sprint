from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response

from src.models.like import Like, FilmRate
from src.services.like import get_likes_service, LikeService

router = APIRouter()


@router.post(
    '',
    description='Save personal film rate to mongo',
    summary='Save personal film rate to mongo',
    response_model=Like,
    # dependencies=[Depends(Access({'admin', 'subscriber'}))],
)
async def create_like(
    like: Like,
    likes_service: LikeService = Depends(get_likes_service),
):
    return await likes_service.create_like(like)


@router.delete(
    '',
    description='Delete like from mongo',
    summary='Delete like from mongo',
    response_class=Response,
    status_code=204,
    # dependencies=[Depends(Access({'admin', 'subscriber'}))],
)
async def delete_bookmark(
    like: Like,
    likes_service: LikeService = Depends(get_likes_service),
):
    return await likes_service.remove_like(like)


@router.get(
    '/{film_id}/rate',
    description='Show average film rate',
    summary='Show average film rate',
    response_model=FilmRate,
    # dependencies=[Depends(Access({'admin', 'subscriber'}))],
)
async def show_average_film_rate(
    film_id: str,
    likes_service: LikeService = Depends(get_likes_service),
):
    return await likes_service.get_film_rate(film_id)


@router.get(
    '/{film_id}',
    description='Show film likes',
    summary='Show film likes',
    response_model=FilmRate,
    # dependencies=[Depends(Access({'admin', 'subscriber'}))],
)
async def get_film_likes(
    film_id: str,
    likes_service: LikeService = Depends(get_likes_service),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1),
):
    return await likes_service.find_all_with_paging({'film_id': film_id}, page, page_size)
