from typing import Dict, Sequence

from pydantic import BaseModel


class GetManyOut(BaseModel):
    total: int
    data: Sequence[Dict]
