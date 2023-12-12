from dtos.search_result import SearchResult
from dtos.match import Match
from dtos.meta_match import MetaMatch
from geojson import GeoJSON
from fastapi.types import Callable
from elastic_transport import ObjectApiResponse
from typing import Optional
from utils.geometry_manipulation import modify_geojson_geometry


def prepare_search_result_for_gb3(index: str, search_result: ObjectApiResponse) -> SearchResult:
    if index == "fme-addresses":
        return get_results(index, search_result, lambda hit_source: f"{hit_source['street']} {hit_source['no']}, "
                                                                    f"{hit_source['plz']} {hit_source['town']}")
    if index == "fme-places":
        return get_results(index, search_result, lambda hit_source: f"{hit_source['type']} {hit_source['name']}")

    if "meta" in index:
        return get_meta_results(index, search_result)

    return get_results(index, search_result, lambda hit_source: get_special_search_display(hit_source))


def get_results(index: str, search_result: ObjectApiResponse,
                display_string_factory: Callable[dict, str]) -> SearchResult:
    matches = []
    hits = search_result["hits"]["hits"]
    for hit in hits:
        hit_source = hit["_source"]
        matches.append(
            Match(
                displayString=display_string_factory(hit_source),
                score=hit["_score"],
                geometry=get_geometry(hit_source)
            )
        )

    return SearchResult(
        index=index,
        matches=matches
    )

def get_meta_results(index: str, search_result: ObjectApiResponse) -> SearchResult:
    matches = []
    hits = search_result["hits"]["hits"]
    for hit in hits:
        hit_source = hit["_source"]
        if "uuid" in hit_source.keys():
            matches.append(
                MetaMatch(
                    uuid=str(hit_source["uuid"]),
                    score=hit["_score"]
                )
            )

    return SearchResult(
        index=index,
        matches=matches
    )


def get_geometry(hit_source: dict) -> Optional[GeoJSON]:
    if hit_source.get("geometry"):
        return modify_geojson_geometry(GeoJSON(hit_source.get("geometry")))

    return None


def get_special_search_display(hit_source: dict) -> str:
    values = []
    fields = [e for e in hit_source.keys() if e != 'geometry']
    for field in fields:
        value = hit_source[field]
        if value is not None:
            values.append(get_display_string(value))

    return " ".join(values)


def get_display_string(value) -> str:
    if isinstance(value, float):
        return f'{value:g}'

    return str(value)
