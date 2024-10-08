from fastapi import FastAPI, HTTPException
from elasticsearch import Elasticsearch
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from utils.query_builder import build_query
from utils.index_utils import get_indexed_field_name
from indexes.search_results import prepare_search_result_for_gb3
from dtos.search_result import SearchResult

load_dotenv()
ELASTIC_PASSWORD = os.getenv('ELASTIC_PASSWORD')
ELASTIC_URL = os.getenv('ELASTIC_URL')
META_INDEX_IDENTIFIER = 'meta'
META_INDEX_QUERY_SIZE = 10000  # Needs to be higher than the maximum number of results delivered by the metadata search

gb3_search = FastAPI()
es = Elasticsearch(
    ELASTIC_URL,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)

gb3_search.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@gb3_search.get("/search")
async def search(indexes: str, term: str) -> list[SearchResult]:
    results = []
    for index in indexes.split(","):
        # https://elasticsearch-py.readthedocs.io/en/v8.10.1/api.html#elasticsearch.Elasticsearch.search
        if index.strip() == "" or "*" in index or "_all" in index:
            raise HTTPException(status_code=400, detail="Empty Index")
        field_name = get_indexed_field_name(es, index)
        query = build_query(field_name, term)
        if META_INDEX_IDENTIFIER in index:
            search_result = es.search(index=index.lower(), query=query.dict(), size=META_INDEX_QUERY_SIZE)
        else:
            search_result = es.search(index=index.lower(), query=query.dict())

        results.append(prepare_search_result_for_gb3(index, search_result, field_name))
    return results
