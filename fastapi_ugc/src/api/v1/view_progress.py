from fastapi import APIRouter

from src.models.view_progress import QueryParams

router = APIRouter()


@router.post(
    '/save',
    description='Save view progress to kafka',
    summary='Save view progress to kafka',
)
async def save_view_progress_to_kafka(
    save_view_progress_to_kafka_params: QueryParams,
):
    return {'res': save_view_progress_to_kafka_params.dict()}
