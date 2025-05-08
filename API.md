# 1R-Micro API Reference

## 🌐 Base URL

```
http://localhost:2691
```

> ℹ️ **Versioning Note**: All current endpoints are under `/v1/`. A versioning strategy ensures backward compatibility. Future changes may introduce `/v2/`, etc.
>
> 📘 **OpenAPI Spec**: A machine-readable OpenAPI 3.1 schema may be available at `/openapi.json` to support automated tooling and SDK generation.

---

## 🏠 GET /v1/

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

**Example:**

```bash
curl http://localhost:2691/v1/objects/urn:1r-micro:abc123 -H "Authorization: Bearer <token>"
```

**Response:** `200 OK`

```json
{
  "@id": "urn:1r-micro:abc123",
  "@type": "Shipment"
}
```

**Errors:**

* `403 Forbidden` if access is denied
* `404 Not Found` if the object does not exist

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

**Curl Example:**

```bash
curl -X POST http://localhost:2691/v1/objects \
  -H "Content-Type: application/json" \
  -H "X-Entity: acme" \
  -d '{"@type":"SensorReading","value":22.5,"entity":"acme"}'
```

---

## ↺ PUT /v1/objects/<object_id>

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

* `403 Forbidden` if access is denied
* `404 Not Found` if the object does not exist

---

## 📾 GET /v1/objects/<object_id>/render

**Description:** Returns a human-readable string representation of the object.

**Query Parameters:**

* `format`: `html`, `md`, or `ascii`

**Curl Example:**

```bash
curl http://localhost:2691/v1/objects/urn:1r-micro:abc123/render?format=md
```

**Response (Markdown):** `200 OK`

```
## SensorReading
- value: 22.5
```

---

## 📬 POST /v1/subscriptions

**Description:** Creates a new event subscription.

```bash
curl -X POST http://localhost:2691/v1/subscriptions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"target":"https://example.com/webhook","filter":{"@type":"SensorReading"},"events":["created"]}'
```

---

## 🗒️ GET /v1/subscriptions

**Description:** Lists all subscriptions for the current entity.

---

## 🗑️ DELETE /v1/subscriptions/<sub_id>

**Description:** Deletes a subscription.

---

## 📣 POST /v1/events

**Description:** Publishes a domain event.

```bash
curl -X POST http://localhost:2691/v1/events \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"@type":"Event","eventType":"arrivedAtGate","object":"urn:1r-micro:ULD456","timestamp":"2025-05-08T16:45:00Z"}'
```

---

## 🔍 GET /v1/whoami

**Description:** Returns information about the current entity.

---

## 🧹 PATCH /v1/objects/<object_id>

**Description:** Partial update using JSON Merge Patch.

---

## 🔐 Auth

Use Bearer token:

```http
Authorization: Bearer <your-token>
```

---

## 🏡 Entity & Visibility

See main spec for details on `entity`, `visibility`, `sharedWith`, `_privateFields`.

---

## ⚡ Curl Summary

```bash
curl -X POST http://localhost:2691/v1/objects \
  -H "Content-Type: application/json" \
  -H "X-Entity: acme" \
  -d '{"@type":"Test","value":123,"entity":"acme"}'

curl http://localhost:2691/v1/objects
curl http://localhost:2691/v1/objects/urn:1r-micro:abc123
curl -X PUT http://localhost:2691/v1/objects/urn:1r-micro:abc123 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"@type":"Test","value":456}'
curl -X DELETE http://localhost:2691/v1/objects/urn:1r-micro:abc123 \
  -H "Authorization: Bearer <token>"
curl http://localhost:2691/v1/objects/urn:1r-micro:abc123/render?format=md
```

---

## Notes

* All requests and responses are in JSON.
* The API is designed to be minimal, secure, and federated.
