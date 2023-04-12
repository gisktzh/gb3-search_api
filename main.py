from fastapi import FastAPI
from elasticsearch import Elasticsearch
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from utils.query_builder import build_query
from indexes.search_results import prepare_search_result_for_gb3

load_dotenv()
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_URL = os.getenv("ELASTIC_URL")

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
async def search(indexes:str, term: str):
    results = []
    for index in indexes.split(","):
        query = build_query(term)
        search_result = es.search(index=index.lower(), query=query)
        results.append(prepare_search_result_for_gb3(index, search_result))
    return results

@gb3_search.get("/indexes")
async def get_all_indexes():
    return es.indices.get_alias(index="*")

@gb3_search.post("/delete")
async def delete_index(index: str):
    es.indices.delete(index=index)