
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