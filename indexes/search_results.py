from typing import List
from classes.search_result import SearchResult
from classes.match import Match
from geojson import Point

def prepare_search_result_for_gb3(index: str, search_result: dict) -> List[SearchResult]:
    if index == "fme-addresses":
        return get_address_results(index, search_result)
    if index == "fme-places":
        return get_places_results(index, search_result)
    return get_special_results(index, search_result)

def get_address_results(index: str, search_result: dict) -> List[SearchResult]:
    matches = []
    hits = search_result["hits"]["hits"]
    for hit in hits:
        hit_source = hit["_source"]
        add_missing_geometry(hit_source)
        matches.append(Match(
            displayString = f"{hit_source['street']} {hit_source['no']}, {hit_source['plz']} {hit_source['town']}",
            score = hit["_score"],
            geometry = Point(hit_source["geometry"])
        ))
    return SearchResult(
        index = index,
        matches = matches
    )

def get_places_results(index: str, search_result: dict) -> List[SearchResult]:
    matches = []
    hits = search_result["hits"]["hits"]
    for hit in hits:
        hit_source = hit["_source"]
        add_missing_geometry(hit_source)
        matches.append(Match(
            displayString = f"{hit_source['type']} {hit_source['name']}",
            score = hit["_score"],
            geometry = Point(hit_source["geometry"])
        ))
    return SearchResult(
        index = index,
        matches = matches
    )

def get_special_results(index: str, search_result: dict) -> List[SearchResult]:
    matches = []
    hits = search_result["hits"]["hits"]
    for hit in hits:
        hit_source = hit["_source"]
        fields = list(hit_source.keys())
        fields.remove("geometry")
        display = get_special_search_display(hit_source, fields)
        add_missing_geometry(hit_source)
        matches.append(Match(
            displayString = display,
            score = hit["_score"],
            geometry = Point(hit_source["geometry"])
        ))
    return SearchResult(
        index = index,
        matches = matches
    )

def add_missing_geometry(hit_source: dict):
    if not hit_source.get("geometry"):
        hit_source["geometry"] = None

def get_special_search_display(hit_source: dict, fields: List[str]) -> str:
    values = []
    for field in fields:
        value = hit_source[field]
        if value is not None:
            values.append(get_display_string(value))
    return " ".join(values)

def get_display_string(value) -> str:
    if isinstance(value, float):
        return f'{value:g}'
    return str(value)
