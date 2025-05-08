# 1R-Micro API Reference

## 🌐 Base URL

```
http://localhost:2691
```

> ℹ️ **Versioning Note**: All current endpoints are under `/v1/`. A versioning strategy ensures backward compatibility. Future changes may introduce `/v2/`, etc.
>
> 📘 **OpenAPI Spec**: A machine-readable OpenAPI 3.1 schema may be available at `/openapi.json` to support automated tooling and SDK generation.

---

## 🏠 GET /

**Returns:** a welcome message to confirm the server is running.

**Response:**

```
Hello from 1R-Micro (Python)
```

---

## 📦 GET /v1/objects

**Description:** Lists all stored JSON-LD objects visible to the requesting entity.

**Response:** `200 OK`

```json
[
  {
    "@id": "urn:1r-micro:abc123",
    "@type": "Shipment"
  }
]
```

---

## 📄 GET /v1/objects/<object_id>

**Description:** Retrieves a single object by its `@id`, subject to visibility and entity-based access control.

**Response:** `200 OK`

```json
{
  "@id": "urn:1r-micro:abc123",
  "@type": "Shipment"
}
```

**Errors:**

- `403 Forbidden` if access is denied
- `404 Not Found` if the object does not exist

---

## 📝 POST /v1/objects

**Description:** Creates a new object.

**Request Body:**

```json
{
  "@type": "SensorReading",
  "@context": "https://example.org/context",
  "value": 22.5,
  "entity": "acme"
}
```

**Response:** `201 Created`

```json
{
  "@id": "urn:1r-micro:generated-id",
  "@type": "SensorReading"
}
```

---

## 🔁 PUT /v1/objects/<object_id>

**Description:** Updates an existing object by `@id`.

**Request Body:**

```json
{
  "@type": "SensorReading",
  "value": 24.8
}
```

**Response:** `200 OK`

```json
{
  "@id": "urn:1r-micro:abc123",
  "@type": "SensorReading",
  "value": 24.8
}
```

---

## ❌ DELETE /v1/objects/<object_id>

**Description:** Deletes the object with the given ID.

**Response:** `200 OK`

```json
{
  "message": "Deleted"
}
```

**Errors:**

- `403 Forbidden` if access is denied
- `404 Not Found` if the object does not exist

---

## 📟 GET /v1/objects/<object_id>/render

**Description:** Returns a human-readable string representation of the object.

**Query Parameters:**

- `format`: Optional. One of `html`, `md`, `ascii`

**Response:** `200 OK`

---

## 📬 POST /v1/subscriptions

**Description:** Creates a new event subscription.

**Request Body:**

```json
{
  "target": "https://example.com/webhook",
  "filter": {
    "@type": "SensorReading",
    "value": { "gt": 100 }
  },
  "events": ["created"],
  "expires_at": "2025-06-01T00:00:00Z"
}
```

**Response:** `201 Created`

```json
{
  "id": "sub-abc123",
  "message": "Subscription created"
}
```

---

## 🗒️ GET /v1/subscriptions

**Description:** Lists all active subscriptions owned by the calling entity.

**Response:** `200 OK`

```json
[
  {
    "id": "sub-abc123",
    "target": "...",
    "filter": { "@type": "SensorReading" }
  }
]
```

---

## 🗑️ DELETE /v1/subscriptions/<sub_id>

**Description:** Deletes a subscription.

**Response:** `200 OK`

```json
{ "message": "Subscription deleted" }
```

**Errors:**

- `403 Forbidden` if the subscription does not belong to the caller
- `404 Not Found` if the subscription does not exist

---

## 📣 POST /v1/events

**Description:** Publishes a user-defined domain event. Triggers pub/sub if filters match.

**Request Body:**

```json
{
  "@type": "Event",
  "eventType": "arrivedAtGate",
  "object": "urn:1r-micro:ULD456",
  "timestamp": "2025-05-08T16:45:00Z"
}
```

**Response:** `201 Created`

---

## 🔍 GET /v1/whoami

**Description:** Returns information about the current authenticated user.

**Response:** `200 OK`

```json
{
  "entity": "acme-corp",
  "roles": ["default"],
  "token_valid": true
}
```

---

## 🧹 PATCH /v1/objects/<object_id>

**Description:** Partially updates an object using JSON Merge Patch.

**Request Body Example:**

```json
{
  "status": "inTransit",
  "location": "Zurich"
}
```

**Response:** `200 OK`

---

## 🔐 Authentication

Clients may use a simulated token for development:

```
Authorization: Bearer acme
```

This is interpreted as setting the request's `entity` to `acme`. No real token validation is performed.

In production, replace this with JWT validation logic.

---

## 🧪 Curl Examples (Simulated Token Mode Only)

### Create an object as entity `acme`

```bash
curl -X POST http://localhost:2691/v1/objects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer acme" \
  -d '{"@type":"SensorReading","value":22.5,"entity":"acme"}'
```

### Get object as entity `acme`

```bash
curl http://localhost:2691/v1/objects/urn:1r-micro:abc123 \
  -H "Authorization: Bearer acme"
```

### Update object as entity `acme`

```bash
curl -X PUT http://localhost:2691/v1/objects/urn:1r-micro:abc123 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer acme" \
  -d '{"@type":"SensorReading","value":24.8}'
```

### Delete object as entity `acme`

```bash
curl -X DELETE http://localhost:2691/v1/objects/urn:1r-micro:abc123 \
  -H "Authorization: Bearer acme"
```

### Render an object in Markdown

```bash
curl http://localhost:2691/v1/objects/urn:1r-micro:abc123/render?format=md \
  -H "Authorization: Bearer acme"
```

### Subscribe to sensor readings

```bash
curl -X POST http://localhost:2691/v1/subscriptions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer acme" \
  -d '{"target": "http://client.example.com/webhook", "filter": {"@type": "SensorReading"}, "events": ["created"]}'
```

### Post a domain event

```bash
curl -X POST http://localhost:2691/v1/events \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer acme" \
  -d '{"@type":"Event","eventType":"arrivedAtGate","object":"urn:1r-micro:ULD456","timestamp":"2025-05-08T16:45:00Z"}'
```

### Check who you are

```bash
curl http://localhost:2691/v1/whoami \
  -H "Authorization: Bearer acme"
```

---

## Notes

- All requests and responses are in JSON.
- The API is intended to be minimal, portable, and federated-ready.
