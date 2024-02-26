from utils.index_utils import get_indexed_field_name
from unittest.mock import MagicMock


def test_returns_index_name_when_no_index_found(es_mock: MagicMock):
    es_mock.indices.get_mapping.return_value = {}
    actual = get_indexed_field_name(es_mock, 'testindex')
    expected = 'testindex'

    assert actual == expected

def test_returns_index_name_when_no_mapping_configured(es_mock: MagicMock):
    es_mock.indices.get_mapping.return_value = {
        'testindex_12345': {}
    }

    actual = get_indexed_field_name(es_mock, 'testindex')
    expected = 'testindex'

    assert actual == expected

def test_get_indexed_field_name_index_att_test(es_mock: MagicMock):
    es_mock.indices.get_mapping.return_value = {
        'testindex_12345': {
            'mappings': {
                'properties': {
                    'geometry': {
                        'type': 'geo_shape'
                    },
                    'index_att_test': {
                        'type': 'text',
                        'analyzer': 'default'
                    }
                }
            }
        }
    }

    actual = get_indexed_field_name(es_mock, 'testindex')
    expected = 'index_att_test'

    assert actual == expected
