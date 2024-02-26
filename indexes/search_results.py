from dtos.search_result import SearchResult
from dtos.match import Match
from dtos.meta_match import MetaMatch
from fastapi.types import Callable
from elastic_transport import ObjectApiResponse
from utils.geometry_utils import get_geometry


def prepare_search_result_for_gb3(index: str, search_result: ObjectApiResponse, field_name: str) -> SearchResult:
    if "meta" in index:
        return get_meta_results(index, search_result)

    return get_results(index, search_result, lambda hit_source: get_display_string(hit_source[field_name]))


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

def get_display_string(value) -> str:
    if isinstance(value, float):
        return f'{value:g}'

    return str(value)
