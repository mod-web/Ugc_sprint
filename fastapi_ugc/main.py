import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


from settings import settings
from src.api.v1 import view_progress

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


app.include_router(view_progress.router, prefix='/api/v1/view_progress', tags=['view_progress'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
