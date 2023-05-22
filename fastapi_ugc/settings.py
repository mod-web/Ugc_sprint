import os
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    project_name: str = Field(..., env='PROJECT_NAME')
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
