from geojson import GeoJSON
from pydantic import BaseModel, ConfigDict
from typing import Optional


class Match(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    displayString: str
    score: float = -1
    geometry: Optional[GeoJSON] = None

