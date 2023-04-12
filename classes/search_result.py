from typing import List
from classes.match import Match

class SearchResult:
    def __init__(self, index: str, matches: List[Match]):
        self.index = index
        self.matches = matches
