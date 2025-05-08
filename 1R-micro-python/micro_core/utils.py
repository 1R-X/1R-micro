from flask import request, Response
import json

# Fake in-memory auth context for now
def get_requesting_entity():
    auth_header = request.headers.get("Authorization", "")
    if auth_header.lower().startswith("bearer "):
        return auth_header[7:].strip()
    return request.headers.get("X-Entity", "public")


def is_authorized(entity, obj):
    if not obj:
        return False
    return obj.get("visibility") == "public" or obj.get("entity") == entity


def redact_object_for(entity, obj):
    if obj.get("visibility") == "public" or obj.get("entity") == entity:
        return obj

    redacted = obj.copy()
    for field in obj.get("_privateFields", []):
        redacted.pop(field, None)
    return redacted



def render_object(obj, fmt="html"):
    if fmt == "md":
        content = f"### {obj.get('@type')}\n\n{obj}"
        return Response(content, mimetype="text/markdown")
    elif fmt == "ascii":
        content = f"{obj.get('@type')}:\n" + "\n".join(f"{k}: {v}" for k, v in obj.items())
        return Response(content, mimetype="text/plain")
    else:  # html
        content = f"<h2>{obj.get('@type')}</h2><pre>{json.dumps(obj, indent=2)}</pre>"
        return Response(content, mimetype="text/html")



def publish_event(event):
    # Stub: in future, push event to relevant subscribers
    print(f"[pubsub] Event published: {event.get('@id', 'unknown')}")
