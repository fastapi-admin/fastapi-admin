from typing import Sequence, Dict
from pydantic import BaseModel


class GetManyOut(BaseModel):
    total: int
    data: Sequence[Dict]
