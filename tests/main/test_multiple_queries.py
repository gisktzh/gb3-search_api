from unittest.mock import MagicMock

import pytest
from starlette.testclient import TestClient

import utils.query_builder


@pytest.mark.skip(reason='fails due to architecture when run in tandem')
def test_calls_elastic_search_for_each_index(es_mock: MagicMock, api_client: TestClient):
    indices = 'index-1,index-2'
    term = 'testterm'
    field_name1 = 'index-1'
    field_name2 = 'index-2'

    api_client.get(
        "/search",
        params={'indexes': indices, 'term': term}
    )

    expected_params = [
        {
            'index': 'index-1',
            'query': utils.query_builder.build_query(field_name1, term).dict()
        },
        {
            'index': 'index-2',
            'query': utils.query_builder.build_query(field_name2, term).dict()
        }
    ]

    assert es_mock.return_value.search.call_count == 2
    es_mock.return_value.search.assert_any_call(**expected_params[0])
    es_mock.return_value.search.assert_any_call(**expected_params[1])
