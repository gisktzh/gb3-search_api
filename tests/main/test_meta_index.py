from unittest.mock import MagicMock

import pytest
from starlette.testclient import TestClient

import utils.query_builder


@pytest.mark.skip(reason='fails due to architecture when run in tandem')
def test_calls_elastic_search_for_each_meta_index_with_specific_size(es_mock: MagicMock, api_client: TestClient):
    index = 'meta-index'
    term = 'testterm'

    api_client.get(
        "/search",
        params={'indexes': index, 'term': term}
    )

    expected_params = {
        'index': index,
        'query': utils.query_builder.build_query(term),
        'size': 10000
    }

    es_mock.return_value.search.assert_called_once_with(**expected_params)
