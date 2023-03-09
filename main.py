from fastapi import FastAPI, HTTPException
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
        else:
            raise HTTPException(status_code=404, detail=f"Search index {index} not found")

    output = {"results": results}
    return output