def build_query(field_name: str, term: str) -> dict:
    return {
        "bool": {
            "should": [
                {
                    "match": {
                        field_name: {
                            "query": term,
                            "fuzziness": "AUTO",
                            "operator": "and",
                            "analyzer": "default_search"
                        }
                    }
                },
                {
                    "match": {
                        "wordstart": {
                            "query": term,
                            "boost": 3,
                            "fuzziness": "AUTO",
                            "operator": "and",
                            "analyzer": "default_search"
                        }
                    }
                }
            ],
            "minimum_should_match": 1
        }
    }
