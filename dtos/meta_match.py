from pydantic import BaseModel


class MetaMatch(BaseModel):
    id: str | None
    score: float = -1
