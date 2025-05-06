import os
import json
import uuid
import yaml


# Load config
CONFIG_PATH = os.environ.get("CONFIG_PATH", os.path.join(os.path.dirname(__file__), '..', 'config.yaml'))
with open(CONFIG_PATH, 'r') as f:
    config = yaml.safe_load(f)

OBJECT_STORE_PATH = config.get("store_path", os.path.join(os.path.dirname(__file__), '..', 'object_store'))
BASE_URI = config.get("base_uri", "urn:1r-micro")

# Ensure storage folder exists
os.makedirs(OBJECT_STORE_PATH, exist_ok=True)

def _get_object_path(object_id):
    """Convert an object ID into a filename."""
    clean_id = object_id.replace(":", "_").replace("/", "_")
    return os.path.join(OBJECT_STORE_PATH, f"{clean_id}.json")

def get_all_objects():
    """Return all stored objects."""
    objects = []
    for filename in os.listdir(OBJECT_STORE_PATH):
        if filename.endswith(".json"):
            with open(os.path.join(OBJECT_STORE_PATH, filename), "r") as f:
                try:
                    obj = json.load(f)
                    objects.append(obj)
                except json.JSONDecodeError:
                    continue
    return objects

def get_object_by_id(object_id):
    """Return a single object by @id."""
    path = _get_object_path(object_id)
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)

def save_object(obj):
    """Save a new or updated object."""
    # Normalize @id
    if "@id" not in obj:
        obj["@id"] = f"{BASE_URI}:{uuid.uuid4()}"
    elif not obj["@id"].startswith(BASE_URI):
        obj["@id"] = f"{BASE_URI}:{obj['@id']}"

    object_id = obj["@id"]
    path = _get_object_path(object_id)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
    return obj

def delete_object(object_id):
    """Delete an object by @id."""
    path = _get_object_path(object_id)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False

def object_exists(object_id):
    """Check if object exists by ID."""
    path = _get_object_path(object_id)
    return os.path.exists(path)
