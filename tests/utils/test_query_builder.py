from utils import query_builder
from enums.fuzziness import Fuzziness
from enums.query_operator import QueryOperator
from dtos.elasticsearch_query import ElasticsearchQuery, ElasticsearchBoolQuery, ElasticsearchShouldItem,\
    ElasticsearchMatchField

def test_generates_correct_query():
    term: str = 'This is a test string'
    field_name: str = 'index_att_test'

    actual: ElasticsearchQuery = query_builder.build_query(field_name, term)

    expected = ElasticsearchQuery(
        bool=ElasticsearchBoolQuery(
            should=[
                ElasticsearchShouldItem(
                    match={
                        field_name: ElasticsearchMatchField(
                            query=term,
                            boost=1,
                            fuzziness=Fuzziness.AUTO,
                            operator=QueryOperator.AND,
                            analyzer="default_search"
                        )
                    }
                ),
                ElasticsearchShouldItem(
                    match={
                        "wordstart": ElasticsearchMatchField(
                            query=term,
                            boost=3,
                            fuzziness=Fuzziness.AUTO,
                            operator=QueryOperator.AND,
                            analyzer="default_search"
                        )
                    }
                )
            ],
            minimum_should_match=1
        )
    )

    assert actual == expected
