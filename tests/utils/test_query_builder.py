from utils import query_builder


def test_generates_correct_query():
    term: str = 'This is a test string'

    actual: dict = query_builder.build_query(term)

    expected: dict = {
        "multi_match": {
            "query": term,
            "type": "cross_fields",
            "fields": ["*"],
            "operator": "and"
        }
    }

    assert actual == expected
