import os
import json
import uuid
import shutil
import pytest
from micro_core import datastore

# Use a temporary test folder for storage
TEST_STORE_PATH = os.path.join(os.path.dirname(__file__), "..", "object_store_test")

def setup_module(module):
    os.makedirs(TEST_STORE_PATH, exist_ok=True)
    datastore.OBJECT_STORE_PATH = TEST_STORE_PATH

def teardown_module(module):
    shutil.rmtree(TEST_STORE_PATH)

def test_save_and_get_object():
    test_id = f"urn:1r-micro:{uuid.uuid4()}"
    obj = {
        "@context": "https://example.org/context",
        "@type": "TestObject",
        "@id": test_id,
        "value": 123
    }
    datastore.save_object(obj)
    retrieved = datastore.get_object_by_id(test_id)
    assert retrieved is not None
    assert retrieved["value"] == 123

def test_get_all_objects():
    all_objects = datastore.get_all_objects()
    assert isinstance(all_objects, list)
    assert any("@id" in obj for obj in all_objects)

def test_delete_object():
    test_id = f"urn:1r-micro:{uuid.uuid4()}"
    obj = {
        "@context": "https://example.org/context",
        "@type": "Deletable",
        "@id": test_id
    }
    datastore.save_object(obj)
    deleted = datastore.delete_object(test_id)
    assert deleted is True
    assert datastore.get_object_by_id(test_id) is None