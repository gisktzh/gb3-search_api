from geojson import MultiPoint, GeoJSON, MultiLineString, MultiPolygon
from utils import geometry_utils


def test_returns_point_for_multipoint_with_1_coordinate():
    coordinates: list = [[0, 1]]
    mock: MultiPoint = MultiPoint(coordinates=coordinates)

    actual: GeoJSON = geometry_utils.modify_geojson_geometry(mock)

    assert actual['type'] == 'Point'
    assert actual['coordinates'] == coordinates[0]


def test_returns_linestring_for_multilinestring_with_1_coordinate():
    coordinates: list = [[[0, 1], [1, 2]]]
    mock: MultiLineString = MultiLineString(coordinates=coordinates)

    actual: GeoJSON = geometry_utils.modify_geojson_geometry(mock)

    assert actual['type'] == 'LineString'
    assert actual['coordinates'] == coordinates[0]


def test_returns_polygon_for_multipolygon_with_1_coordinate():
    coordinates: list = [[[0, 1], [1, 2]]]
    mock: MultiPolygon = MultiPolygon(coordinates=coordinates)

    actual: GeoJSON = geometry_utils.modify_geojson_geometry(mock)

    assert actual['type'] == 'Polygon'
    assert actual['coordinates'] == coordinates[0]


def test_returns_input_for_real_multi_geometry():
    coordinates: list = [[[0, 1], [1, 2]], [[2, 4], [4, 1]]]
    mock: MultiPolygon = MultiPolygon(coordinates=coordinates)

    actual: GeoJSON = geometry_utils.modify_geojson_geometry(mock)

    assert actual['type'] == 'MultiPolygon'
    assert actual['coordinates'] == coordinates


def test_get_geometry_if_input_has_valid_geojson():
    coordinates: list =[[0, 1]]
    mock_geometry: MultiPoint = MultiPoint(coordinates=coordinates)

    mock_hit_source: dict = {"geometry": mock_geometry}

    actual: GeoJSON = geometry_utils.get_geometry(mock_hit_source)

    assert actual['type'] == 'Point'
    assert actual['coordinates'] == coordinates[0]


def test_get_geometry_if_input_has_valid_dict():
    coordinates: list =[[0, 1]]
    mock_geometry: dict = {"type": "MultiPoint", "coordinates": coordinates}

    mock_hit_source: dict = {"geometry": mock_geometry}
    actual: GeoJSON = geometry_utils.get_geometry(mock_hit_source)

    assert actual['type'] == 'Point'
    assert actual['coordinates'] == coordinates[0]
