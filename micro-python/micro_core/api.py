from flask import Blueprint, request, jsonify
from micro_core import datastore
import uuid

api = Blueprint('api', __name__)

@api.route("/", methods=["GET"])
def index():
    return "Hello from 1R-Micro (Python)"

@api.route("/objects", methods=["GET"])
def get_all_objects():
    objects = datastore.get_all_objects()
    return jsonify(objects), 200

@api.route("/objects/<object_id>", methods=["GET"])
def get_object(object_id):
    obj = datastore.get_object_by_id(object_id)
    if obj:
        return jsonify(obj), 200
    else:
        return jsonify({"error": "Object not found"}), 404

@api.route("/objects", methods=["POST"])
def create_object():
    obj = request.get_json(force=True)

    # Assign a unique @id if missing
    if "@id" not in obj:
        obj["@id"] = f"urn:1r-micro:{uuid.uuid4()}"

    saved = datastore.save_object(obj)
    return jsonify(saved), 201
