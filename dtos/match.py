from geojson import GeoJSON
from pydantic import BaseModel
from typing import Optional

class Match(BaseModel):
    displayString: str
    score: float = -1
    geometry: Optional[GeoJSON] = None
