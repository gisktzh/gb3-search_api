def build_query(term: str) -> dict:
    return {
        "multi_match": {
            "query": term,
            "type": "cross_fields",
            "fields": ["*"],
            "operator": "and"
        }
    }

def build_meta_query(term: str) -> dict:
    return {
        "size": 1000,
        "multi_match": {
            "query": term,
            "type": "cross_fields",
            "fields": ["*"],
            "operator": "and"
        }
    }
