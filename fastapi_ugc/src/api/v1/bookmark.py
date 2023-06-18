from fastapi import APIRouter, Depends

from src.models.bookmark import BookMark, BookMarkResponse
from src.services.bookmark import get_bookmarks_service, BookMarkService

router = APIRouter()


@router.post(
    '',
    description='Save bookmark to mongo',
    summary='Save bookmark to mongo',
    response_model=BookMarkResponse,
    # dependencies=[Depends(Access({'admin', 'subscriber'}))],
)
async def save_view_bookmark_to_mongo(
    bookmark_data: BookMark,
    bookmarks_service: BookMarkService = Depends(get_bookmarks_service),
):
    result = await bookmarks_service.insert_one(bookmark_data.dict())
    return result
