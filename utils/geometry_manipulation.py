from geojson import GeoJSON

def modify_geojson_geometry(input_geometry: GeoJSON) -> GeoJSON:
    """
    Elasticsearch always returns MultiGeometries, even if it's just one Point/Line/Polygon. This function makes sure that
    only actual MultiGeometries are sent as MultiGeometries, while single geometries are handled as such.
    """
    if len(input_geometry['coordinates']) == 1:
        if input_geometry['type'] == 'MultiPoint':
            return GeoJSON({
                "type": 'Point',
                "coordinates": input_geometry['coordinates'][0]
            })
        elif input_geometry['type'] == 'MultiLineString':
            return GeoJSON({
                "type": 'LineString',
                "coordinates": input_geometry['coordinates'][0]
            })
        elif input_geometry['type'] == 'MultiPolygon':
            return GeoJSON({
                "type": 'Polygon',
                "coordinates": input_geometry['coordinates'][0]
            })
        else:
            return input_geometry

    return input_geometry
