def build_query(term: str) -> dict:     
    return {
        "multi_match":{
            "query":term,
            "type":"cross_fields",
            "fields":["*"]
        }
    }