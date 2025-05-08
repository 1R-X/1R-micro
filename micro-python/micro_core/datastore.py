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
    clean_id = object_id.replace(":", "_").replace("/", "_")
    return os.path.join(OBJECT_STORE_PATH, f"{clean_id}.json")


def get_all_objects():
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
    path = _get_object_path(object_id)
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)


def save_object(obj):
    if "@id" not in obj:
        obj["@id"] = f"{BASE_URI}:{uuid.uuid4()}"
    elif not obj["@id"].startswith(BASE_URI):
        obj["@id"] = f"{BASE_URI}:{obj['@id']}"

    path = _get_object_path(obj["@id"])
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
    return obj


def delete_object(object_id):
    path = _get_object_path(object_id)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False


def object_exists(object_id):
    return os.path.exists(_get_object_path(object_id))


# -- Events --

def save_event(event):
    event_id = event.get("@id", f"{BASE_URI}:event:{uuid.uuid4()}")
    event["@id"] = event_id
    return save_object(event)


# -- Subscriptions --

def _subscriptions_path():
    return os.path.join(OBJECT_STORE_PATH, "_subscriptions.json")


def save_subscription(sub):
    subs = get_all_subscriptions()
    sub_id = f"sub-{uuid.uuid4()}"
    sub["id"] = sub_id
    subs.append(sub)
    with open(_subscriptions_path(), "w") as f:
        json.dump(subs, f, indent=2)
    return sub


def get_all_subscriptions():
    path = _subscriptions_path()
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []


def get_subscriptions_by_entity(entity):
    return [s for s in get_all_subscriptions() if s.get("entity") == entity]


def get_subscription(sub_id):
    for s in get_all_subscriptions():
        if s.get("id") == sub_id:
            return s
    return None


def delete_subscription(sub_id):
    subs = get_all_subscriptions()
    updated = [s for s in subs if s.get("id") != sub_id]
    if len(updated) == len(subs):
        return False
    with open(_subscriptions_path(), "w") as f:
        json.dump(updated, f, indent=2)
    return True
