from pydantic import BaseModel


class MetaMatch(BaseModel):
    uuid: str
    score: float = -1
