from flask import Flask, request, jsonify
import uuid
import os
import json

app = Flask(__name__)
STORE_DIR = "./object_store"

# Ensure the local object store exists
if not os.path.exists(STORE_DIR):
    os.makedirs(STORE_DIR)

# Health check route
@app.route("/", methods=["GET"])
def home():
    return "Hello from 1R-Micro", 200

# List all stored logistics objects
@app.route("/objects", methods=["GET"])
def list_objects():
    print("==> Received GET /objects")
    objects = []
    for fname in os.listdir(STORE_DIR):
        with open(os.path.join(STORE_DIR, fname)) as f:
            objects.append(json.load(f))
    return jsonify(objects)

# Create a new logistics object
@app.route("/objects", methods=["POST"])
def create_object():
    print("==> Received POST /objects")
    try:
        obj = request.get_json(force=True)
        print("Parsed JSON:", obj)
        object_id = str(uuid.uuid4())
        obj["@id"] = f"urn:1r-micro:{object_id}"
        with open(os.path.join(STORE_DIR, f"{object_id}.json"), "w") as f:
            json.dump(obj, f, indent=2)
        return jsonify(obj), 201
    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)}), 500

# Retrieve a specific object by ID
@app.route("/objects/<object_id>", methods=["GET"])
def get_object(object_id):
    print(f"==> Received GET /objects/{object_id}")
    try:
        with open(os.path.join(STORE_DIR, f"{object_id}.json")) as f:
            obj = json.load(f)
        return jsonify(obj)
    except FileNotFoundError:
        return jsonify({"error": "Object not found"}), 404

if __name__ == "__main__":
    print("Starting 1R-Micro Server on http://localhost:5001")
    app.run(debug=True, host="0.0.0.0", port=5001)
