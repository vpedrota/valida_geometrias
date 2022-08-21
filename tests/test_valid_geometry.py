
from urllib import response
import pytest
from source import app
import json

@pytest.fixture
def client():
  server = app.create_app()
  server.config['TESTING'] = True

  with server.app_context():
    with server.test_client() as client:
      yield client

def test_too_few_points(client):
   geoJson = json.loads('{"type":"Polygon","coordinates":[[[2,2],[8,2]]]}')
   response = client.post("http://127.0.0.1:5000/", json=geoJson)
   assert response.status_code == 400
   assert json.loads(response.data)['detail'] == "geometry requires more points\n"

def test_nested_holes(client):
    geoJson = json.loads('{"type":"Polygon","coordinates":[[[0,0],[10,0],[10,10],[0,10],[0,0]],[[2,2],[2,8],[8,8],[8,2],[2,2]],[[3,3],[3,7],[7,7],[7,3],[3,3]]]}')
    response = client.post("http://127.0.0.1:'5000/", json=geoJson)
    assert response.status_code == 400
    assert json.loads(response.data)['detail'] == "Holes are nested[3 3]"

def test_disconneected_interior(client):
    geoJson = json.loads('{"type":"Polygon","coordinates":[[[0,0],[10,0],[10,10],[0,10],[0,0]],[[5,0],[10,5],[5,10],[0,5],[5,0]]]}')
    response = client.post("http://127.0.0.1:500'0/", json=geoJson)
    assert response.status_code == 400
    assert json.loads(response.data)['detail'] == "Interior is disconnected[10 5]"

def test_self_intersection(client):
    geoJson = json.loads('{"type":"Polygon","coordinates":[[[0,0],[10,0],[10,10],[0,10],[0,0]],[[5,0],[10,5],[5,10],[0,5],[5,0]],[[5,5],[5,10],[10,5],[5,5]]]}')
    response = client.post("http://127.0.0.1:5000/", json=geoJson)
    assert response.status_code == 400
    assert json.loads(response.data)['detail'] == "Self-intersection[5 10]"

def test_nested_shells(client):
    geoJson = json.loads('{"type":"MultiPolygon","coordinates":[[[[0,0],[10,0],[10,10],[0,10],[0,0]]],[[[2,2],[8,2],[8,8],[2,8],[2,2]]]]}')
    response = client.post("http://127.0.0.1:5000/", json=geoJson)
    assert response.status_code == 400
    assert json.loads(response.data)['detail'] == "Nested shells[2 2]"

def test_duplicated_rings(client):
    geoJson = json.loads('{"type":"MultiPolygon","coordinates":[[[[0,0],[10,0],[10,10],[0,10],[0,0]]],[[[0,0],[10,0],[10,10],[0,10],[0,0]]]]}')
    response = client.post("http://127.0.0.1:5000/", json=geoJson)
    assert response.status_code == 400
    assert json.loads(response.data)['detail'] == "Duplicate Rings[0 0]"

def test_invalid_coordinate(client):
    geoJson = json.loads('{"type":"Polygon","coordinates":[[[NaN,3],[3,4],[4,4],[4,3],[3,3]]]}')
    response = client.post("http://127.0.0.1:5000/", json=geoJson)
    assert response.status_code == 400
    assert json.loads(response.data)['detail'] == "geometry contains non-closed rings\n"

def test_invalid_coordinate_2(client):
    geoJson = json.loads('{"type":"Polygon","coordinates":[[[0,0],[10,0],[10,10],[0,10],[0,0]],[[NaN,3],[3,4],[4,4],[4,3],[3,3]]]}')
    response = client.post("http://127.0.0.1:5000/", json=geoJson)
    assert response.status_code == 400
    assert json.loads(response.data)['detail'] == "geometry contains non-closed rings\n"