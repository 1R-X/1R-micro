import os
import json

# Default folder for object storage
OBJECT_STORE_PATH = os.path.join(os.path.dirname(__file__), '..', 'object_store')

# Ensure storage folder exists
os.makedirs(OBJECT_STORE_PATH, exist_ok=True)

def object_exists(object_id):
    """Check if an object file already exists."""
    path = _get_object_path(object_id)
    return os.path.exists(path)

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
    object_id = obj["@id"]
    path = _get_object_path(object_id)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
    return obj

def delete_object(object_id):
    """Delete an object file by its ID."""
    path = _get_object_path(object_id)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False
