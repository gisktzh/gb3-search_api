from utils import query_builder
from enums.fuzziness import Fuzziness
from enums.query_operator import QueryOperator


def test_generates_correct_query():
    term: str = 'This is a test string'
    field_name: str = 'index_att_test'

    actual: dict = query_builder.build_query(field_name, term).dict()

    expected: dict = {
        "bool": {
            "should": [
                {
                    "match": {
                        field_name: {
                            "query": term,
                            "boost": 1,
                            "fuzziness": Fuzziness.AUTO,
                            "operator": QueryOperator.AND,
                            "analyzer": "default_search"
                        }
                    }
                },
                {
                    "match": {
                        "wordstart": {
                            "query": term,
                            "boost": 3,
                            "fuzziness": Fuzziness.AUTO,
                            "operator": QueryOperator.AND,
                            "analyzer": "default_search"
                        }
                    }
                }
            ],
            "minimum_should_match": 1
        }
    }

    assert actual == expected
