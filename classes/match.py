from geojson import Point

class Match:
    def __init__(self, displayString: str, score: float, geometry: Point):
        self.displayString = displayString
        self.score = score
        self.geometry = geometry
