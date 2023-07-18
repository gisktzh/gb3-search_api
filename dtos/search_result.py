from dtos.match import Match
from dtos.meta_match import MetaMatch
from pydantic import BaseModel


class SearchResult(BaseModel):
    index: str
    matches: list[Match | MetaMatch] = []
