import pytest
import json
from micro_core.api import api
from flask import Flask

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(api)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello from 1R-Micro" in response.data

def test_create_and_get_object(client):
    obj = {
        "@context": "https://example.org/context",
        "@type": "TestObject",
        "name": "Sample"
    }
    response = client.post("/objects", data=json.dumps(obj), content_type="application/json")
    assert response.status_code == 201
    returned = response.get_json()
    object_id = returned["@id"]

    get_response = client.get(f"/objects/{object_id}")
    assert get_response.status_code == 200
    fetched = get_response.get_json()
    assert fetched["@id"] == object_id
    assert fetched["name"] == "Sample"

def test_update_object(client):
    obj = {
        "@context": "https://example.org/context",
        "@type": "Updatable",
        "value": 10
    }
    post_response = client.post("/objects", data=json.dumps(obj), content_type="application/json")
    object_id = post_response.get_json()["@id"]

    updated_obj = {
        "@context": "https://example.org/context",
        "@type": "Updatable",
        "value": 20
    }
    put_response = client.put(f"/objects/{object_id}", data=json.dumps(updated_obj), content_type="application/json")
    assert put_response.status_code == 200
    assert put_response.get_json()["value"] == 20

def test_delete_object(client):
    obj = {
        "@context": "https://example.org/context",
        "@type": "ToDelete",
        "key": "value"
    }
    post_response = client.post("/objects", data=json.dumps(obj), content_type="application/json")
    object_id = post_response.get_json()["@id"]

    delete_response = client.delete(f"/objects/{object_id}")
    assert delete_response.status_code == 200

    follow_up = client.get(f"/objects/{object_id}")
    assert follow_up.status_code == 404
