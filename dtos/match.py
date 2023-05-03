from geojson import Point
from pydantic import BaseModel

class Match(BaseModel):
    displayString: str
    score: float = -1
    geometry: Point | None = None
