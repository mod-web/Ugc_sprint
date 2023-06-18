from typing import List


from src.models.base import Paginated, Base


class BookMarkResponse(Base):
    id: str


class BookMarkResponseList(Paginated):
    data: List[BookMarkResponse]
