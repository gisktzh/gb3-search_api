from unittest.mock import MagicMock

from starlette.testclient import TestClient

import utils.query_builder


def test_calls_elastic_search_with_index_and_query(es_mock: MagicMock, api_client: TestClient):
    index = 'textindex'
    term = 'testterm'
    field_name = index

    api_client.get(
        "/search",
        params={'indexes': index, 'term': term}
    )

    expected_params = {
        'index': index,
        'query': utils.query_builder.build_query(field_name, term)
    }

    es_mock.return_value.search.assert_called_once()
    es_mock.return_value.search.assert_called_with(**expected_params)
