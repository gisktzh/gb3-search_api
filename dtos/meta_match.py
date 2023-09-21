from pydantic import BaseModel
from typing import Optional


class MetaMatch(BaseModel):
    uuid: Optional[str]
    score: float = -1
