from dtos.match import Match
from pydantic import BaseModel

class SearchResult(BaseModel):
    index: str
    matches: list[Match] = []
