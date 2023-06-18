from pydantic import BaseModel


class Paginated(BaseModel):
    total_count: int
    page: int
