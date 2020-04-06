from typing import Sequence, Dict
from pydantic import BaseModel


class GetManyOut(BaseModel):
    total: int
    per_page: int = 10
    page: int = 1
    data: Sequence[Dict]

    class Config:
        fields = {
            'per_page': 'perPage'
        }
