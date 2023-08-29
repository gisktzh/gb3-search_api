from geojson import GeoJSON
from pydantic import BaseModel


class Match(BaseModel):
    displayString: str
    score: float = -1
    geometry: GeoJSON | None = None
