from dtos.elasticsearch_query import ElasticsearchQuery


def build_query(field_name: str, term: str) -> ElasticsearchQuery:
    return ElasticsearchQuery.create_query(field_name, term)
