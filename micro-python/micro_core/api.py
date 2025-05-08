from flask import Blueprint, request, jsonify, current_app as app
from micro_core import datastore, utils
import uuid

api = Blueprint('api', __name__)

@api.route("/", methods=["GET"])
def index():
    return "Hello from 1R-Micro (Python)"

@api.route("/v1/objects", methods=["GET"])
def get_all_objects():
    objects = datastore.get_all_objects()
    entity = utils.get_requesting_entity()
    redacted = [utils.redact_object_for(entity, o) for o in objects]
    return jsonify(redacted), 200

@api.route("/v1/objects/<object_id>", methods=["GET"])
def get_object(object_id):
    obj = datastore.get_object_by_id(object_id)
    if not obj:
        return jsonify({"error": "Object not found"}), 404

    entity = utils.get_requesting_entity()
    if not utils.is_authorized(entity, obj):
        return jsonify({"error": "Forbidden"}), 403

    return jsonify(utils.redact_object_for(entity, obj)), 200

@api.route("/v1/objects", methods=["POST"])
def create_object():
    try:
        obj = request.get_json(force=True)
        if "@id" not in obj:
            obj["@id"] = f"urn:1r-micro:{uuid.uuid4()}"
        if 'linkedTo' in obj and not isinstance(obj['linkedTo'], list):
            obj['linkedTo'] = [obj['linkedTo']]

        # Access control: entity must match token
        caller = utils.get_requesting_entity()
        if 'entity' in obj and obj['entity'] != caller:
            return jsonify({"error": "Entity mismatch"}), 403

        saved = datastore.save_object(obj)
        return jsonify(saved), 201
    except Exception as e:
        app.logger.error(f"Error creating object: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@api.route("/v1/objects/<object_id>", methods=["PUT"])
def update_object(object_id):
    if not datastore.object_exists(object_id):
        return jsonify({"error": "Object not found"}), 404

    updated_obj = request.get_json(force=True)
    updated_obj["@id"] = object_id

    # Access check
    entity = utils.get_requesting_entity()
    if not utils.is_authorized(entity, updated_obj):
        return jsonify({"error": "Forbidden"}), 403

    saved = datastore.save_object(updated_obj)
    return jsonify(saved), 200

@api.route("/v1/objects/<object_id>", methods=["PATCH"])
def patch_object(object_id):
    obj = datastore.get_object_by_id(object_id)
    if not obj:
        return jsonify({"error": "Object not found"}), 404

    entity = utils.get_requesting_entity()
    if not utils.is_authorized(entity, obj):
        return jsonify({"error": "Forbidden"}), 403

    patch_data = request.get_json(force=True)
    merged = obj.copy()
    merged.update(patch_data)
    saved = datastore.save_object(merged)
    return jsonify(saved), 200


@api.route("/v1/objects/<object_id>/render", methods=["GET"])
def render_object(object_id):
    obj = datastore.get_object_by_id(object_id)
    if not obj:
        return jsonify({"error": "Object not found"}), 404

    fmt = request.args.get("format", "html")
    return utils.render_object(obj, fmt)  # ← no ", 200"


@api.route("/v1/events", methods=["POST"])
def post_event():
    event = request.get_json(force=True)
    if not event.get("@type") == "Event" or "object" not in event:
        return jsonify({"error": "Invalid event payload"}), 400

    saved = datastore.save_event(event)
    utils.publish_event(event)  # optional pub/sub hook
    return jsonify(saved), 201


@api.route("/v1/subscriptions", methods=["POST"])
def create_subscription():
    sub = request.get_json(force=True)
    entity = utils.get_requesting_entity()
    sub["entity"] = entity
    saved = datastore.save_subscription(sub)
    return jsonify(saved), 201


@api.route("/v1/subscriptions", methods=["GET"])
def get_subscriptions():
    entity = utils.get_requesting_entity()
    subs = datastore.get_subscriptions_by_entity(entity)
    return jsonify(subs), 200


@api.route("/v1/subscriptions/<sub_id>", methods=["DELETE"])
def delete_subscription(sub_id):
    sub = datastore.get_subscription(sub_id)
    entity = utils.get_requesting_entity()
    if not sub:
        return jsonify({"error": "Not found"}), 404
    if sub.get("entity") != entity:
        return jsonify({"error": "Forbidden"}), 403

    success = datastore.delete_subscription(sub_id)
    return jsonify({"message": "Deleted"}) if success else jsonify({"error": "Delete failed"}), 500


@api.route("/v1/whoami", methods=["GET"])
def whoami():
    entity = utils.get_requesting_entity()
    if not entity:
        return jsonify({"error": "unauthenticated"}), 401
    return jsonify({
        "entity": entity,
        "roles": ["default"],
        "token_valid": True
    }), 200


@api.route("/v1/objects/<object_id>", methods=["DELETE"])
def delete_object(object_id):
    obj = datastore.get_object_by_id(object_id)
    entity = utils.get_requesting_entity()
    if not obj:
        return jsonify({"error": "Object not found"}), 404
    if not utils.is_authorized(entity, obj):
        return jsonify({"error": "Forbidden"}), 403

    success = datastore.delete_object(object_id)
    return (jsonify({"message": "Deleted"}), 200) if success else (jsonify({"error": "Deletion failed"}), 500)
