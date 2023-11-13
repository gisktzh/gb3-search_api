from unittest import mock

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient


@pytest.fixture(scope='function')
def es_mock():
    with mock.patch('elasticsearch.Elasticsearch') as m:
        yield m
        m.reset_mock()


@pytest.fixture(scope='function')
def api_client(es_mock):
    from main import gb3_search
    with TestClient(gb3_search) as client:
        yield client
        del client
