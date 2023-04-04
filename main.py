from fastapi import FastAPI, HTTPException
from elasticsearch import Elasticsearch
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

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
    output = {}
    results = []
    for index in indexes.split(","):
        if index == "fme-addresses":
            query_body = {
                "query":{
                    "multi_match":{
                        "query":term,
                        "type":"cross_fields",
                        "fields":[
                            "street",
                            "no",
                            "town"
                        ]
                    }
                }
            }
        elif index == "fme-places":
            query_body = {
                "query":{
                    "multi_match":{
                        "query":term,
                        "fields":[
                            "name"
                        ]
                    }
                }
            }
        else:
            raise HTTPException(status_code=404, detail=f"Search index {index} not found")
        try:
            search_result = es.search(index=index, body=query_body)
            results.append(
                {
                    "id": index,
                    "data": search_result
                }
            )
        except Exception as e:
            results.append(
                {
                    "id": index,
                    "data": e.body
                }
            )

    output = {"results": results}
    return output
