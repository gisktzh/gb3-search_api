from utils import query_builder


def test_generates_correct_query():
    term: str = 'This is a test string'
    field_name: str = 'index_att_test'

    actual: dict = query_builder.build_query(field_name, term)

    expected: dict = {
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

    assert actual == expected
