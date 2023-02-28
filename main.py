from fastapi import FastAPI
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()
ELASTIC_PASSWORD= os.getenv("ELASTIC_PASSWORD")

gb3_search = FastAPI()
es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", ELASTIC_PASSWORD)
)

@gb3_search.get("/addresses")
async def address_search(search_term: str):
    index = "fme-addresses"

    query_body = {
        "query":{
            "multi_match":{
                "query":search_term,
                "type":"cross_fields",
                "fields":[
                    "street",
                    "no",
                    "town"
                ]
            }
        }
    }
    search_result = es.search(index=index, body=query_body)
    return search_result