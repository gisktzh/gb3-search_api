import pytest


@pytest.mark.parametrize('test_input', [
    'test1,,test2',
    'test1,*,test2',
    'test1,_all,test2',
    'test1,    ,test2',
    'index-1,wild*card,test'
    ',',
    '   ',
    ''
])
def test_returns_400_for_empty_or_wildcard_indices(es_mock, api_client, test_input):
    response = api_client.get(
        "/search",
        params={'indexes': test_input, 'term': 'test'}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Empty Index'}

