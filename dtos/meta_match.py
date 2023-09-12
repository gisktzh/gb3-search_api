from pydantic import BaseModel
from typing import Optional


class MetaMatch(BaseModel):
    id: Optional[str]
    score: float = -1
