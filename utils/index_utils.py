from elasticsearch import Elasticsearch

INDEX_ATT_IDENTIFIER = 'index_att'

def get_indexed_field_name(es: Elasticsearch, index: str) -> str:
    field_map = es.indices.get_mapping(index=index.lower())
    index_name_with_guid = list(field_map)[0]
    field_list = list(field_map[index_name_with_guid]['mappings']['properties'])

    return next(field for field in field_list if INDEX_ATT_IDENTIFIER in field)
