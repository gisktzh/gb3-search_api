from pydantic import BaseModel
from typing import Optional
from enums.fuzziness import Fuzziness
from enums.query_operator import QueryOperator


# See documentation at https://www.elastic.co/guide/en/elasticsearch/reference/7.17/query-dsl-bool-query.html
class ElasticsearchMatchField(BaseModel):
    query: str
    fuzziness: Fuzziness
    operator: QueryOperator
    analyzer: str
    boost: Optional[int] = 1

class ElasticsearchShouldItem(BaseModel):
    match: dict[str, ElasticsearchMatchField]

class ElasticsearchBoolQuery(BaseModel):
    should: list[ElasticsearchShouldItem]
    minimum_should_match: int

class ElasticsearchQuery(BaseModel):
    bool: ElasticsearchBoolQuery

    @classmethod
    def create_query(cls, field_name: str, term: str) -> "ElasticsearchQuery":
        field1 = ElasticsearchMatchField(
            query=term,
            fuzziness=Fuzziness.AUTO,
            operator=QueryOperator.AND,
            analyzer="default_search"
        )

        field2 = ElasticsearchMatchField(
            query=term,
            fuzziness=Fuzziness.AUTO,
            operator=QueryOperator.AND,
            analyzer="default_search",
            boost=3
        )

        should_item1 = ElasticsearchShouldItem(match={field_name: field1})
        should_item2 = ElasticsearchShouldItem(match={field_name: field2})

        bool_query = ElasticsearchBoolQuery(
            should=[should_item1, should_item2],
            minimum_should_match=1
        )

        return cls(bool=bool_query)
