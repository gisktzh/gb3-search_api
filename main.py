from fastapi import FastAPI
from elasticsearch import Elasticsearch
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from utils.query_builder import build_query
from indexes.search_results import prepare_search_result_for_gb3
from dtos.search_result import SearchResult

load_dotenv()
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_URL = os.getenv("ELASTIC_URL")
META_INDEX_IDENTIFIER = 'meta'
META_INDEX_QUERY_SIZE = 1000 # Might need to be increased in the future if the metadata search could potentially have more hits

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
        query = build_query(term)
        if META_INDEX_IDENTIFIER in index:
            search_result = es.search(index=index.lower(), query=query, size=META_INDEX_QUERY_SIZE)
        else:
            search_result = es.search(index=index.lower(), query=query)

        results.append(prepare_search_result_for_gb3(index, search_result))
    return results
