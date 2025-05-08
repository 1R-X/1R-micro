# 1R-Micro API Reference

## 🌐 Base URL

```
http://localhost:2691
```

> ℹ️ **Versioning Note**: All current endpoints are under `/v1/`. A versioning strategy ensures backward compatibility. Future changes may introduce `/v2/`, etc.
>
> 📘 **OpenAPI Spec**: A machine-readable OpenAPI 3.1 schema may be available at `/openapi.json` to support automated tooling and SDK generation.

> Note: A versioning strategy (e.g., `/v1/...`) may be introduced in future releases.
> A machine-readable OpenAPI 3.1 schema may be available at `/openapi.json` (planned).

---

## 🏠 GET /

**Returns:** a welcome message to confirm the server is running.

**Response:**

```
Hello from 1R-Micro (Python)
```

---

## 📦 GET /objects

**Description:** Lists all stored JSON-LD objects visible to the requesting entity.

**Response:** `200 OK`

```json
[
  {
    "@id": "urn:1r-micro:abc123",
    "@type": "Shipment",
    ...
  },
  ...
]
```

---

## 📄 GET /objects/\<object\_id>

**Description:** Retrieves a single object by its `@id`, subject to visibility and entity-based access control.

**Example:**

```
GET /objects/urn:1r-micro:abc123
```

**Response:** `200 OK`

```json
{
  "@id": "urn:1r-micro:abc123",
  "@type": "Shipment",
  ...
}
```

**Errors:**

* `403 Forbidden` if access is denied
* `404 Not Found` if the object does not exist

---

## 📝 POST /objects

**Description:** Creates a new object.

* If `@id` is missing, a URN will be auto-generated.
* If provided, the `@id` will be normalized to base\_uri if needed.
* The request must match the caller's authenticated entity (if applicable).

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
  "@type": "SensorReading",
  ...
}
```

---

## 🔄 PUT /objects/\<object\_id>

**Description:** Updates an existing object by `@id`.

* The request URL defines the object `@id`, which overrides any `@id` in the body.
* Only the owning entity may modify the object.

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

## ❌ DELETE /objects/\<object\_id>

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

## 🧾 GET /objects/\<object\_id>/render

**Description:** Returns a human-readable string representation of the object.
Supports output formats: `html` (default), `md`, or `ascii`.

**Query Parameters:**

* `format`: Optional. One of `html`, `md`, `ascii`

**Example:**

```
GET /objects/urn:1r-micro:abc123/render?format=md
```

**Response (Markdown):** `200 OK`

```
## SensorReading
- value: 22.5
```

**Errors:**

* `404 Not Found` if the object does not exist
* `400 Bad Request` if format is unsupported

---

## 📬 POST /subscriptions

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

## 🗒️ GET /subscriptions

**Description:** Lists all active subscriptions owned by the calling entity.

**Response:** `200 OK`

```json
[
  {
    "id": "sub-abc123",
    "target": "...",
    "filter": { "@type": "SensorReading" },
    ...
  }
]
```

---

## 🗑️ DELETE /subscriptions/\<sub\_id>

**Description:** Deletes a subscription.

**Response:** `200 OK`

```json
{ "message": "Subscription deleted" }
```

**Errors:**

* `403 Forbidden` if the subscription does not belong to the caller
* `404 Not Found` if the subscription does not exist

---

## 📣 POST /events

**Description:** Publishes a user-defined domain event. Triggers pub/sub if filters match.

* The `object` field must reference an existing object by its `@id`. Posting an event does **not** create or modify the referenced object.

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

```json
{
  "@id": "urn:1r-micro:event-xyz",
  "eventType": "arrivedAtGate",
  ...
}
```

---

## 🔍 GET /whoami

**Description:** Returns information about the current authenticated user (i.e., the resolved entity).

**Response:** `200 OK`

```json
{
  "entity": "acme-corp",
  "roles": ["default"],
  "token_valid": true
}
```

**Errors:**

* `401 Unauthorized` if no valid token is provided

---

## 🧩 PATCH /objects/\<object\_id>

**Description:** Partially updates an object using [JSON Merge Patch (RFC 7396)](https://tools.ietf.org/html/rfc7396).

* Only the fields included in the request will be updated.
* Nested objects will be **fully replaced** unless all fields are included.
* Only the owning entity may modify the object.

**Headers:**

```
Content-Type: application/merge-patch+json
Authorization: Bearer <token>
```

**Request Body Example:**

```json
{
  "status": "inTransit",
  "location": "Zurich"
}
```

**Response:** `200 OK`

```json
{
  "@id": "urn:1r-micro:abc123",
  "@type": "Shipment",
  "status": "inTransit",
  "location": "Zurich",
  ...
}
```

**Errors:**

* `403 Forbidden` if not the object owner
* `404 Not Found` if the object does not exist

---

## 🔐 Authentication

API clients may authenticate using a bearer token:

```http
Authorization: Bearer <your-token>
```

This token determines the `entity` context for all API calls. If omitted, requests are treated as unauthenticated.

> ⚠️ **Warning**: In development mode, unauthenticated access may allow full public access. This is not recommended for production deployments.

---

## 🛡️ Entity Context and Access Control

1R-Micro supports multi-entity deployments where multiple organizations or users ("entities") share a single server instance.

### 🔑 Entity Field

Each object can include an `entity` field to indicate ownership or authorship:

```json
{
  "@type": "SensorReading",
  "value": 22.5,
  "entity": "acme-corp"
}
```

### 🔐 Access Control

The server enforces:

* Create/update/delete permissions per entity
* Read restrictions based on object `entity`
* Subscription filtering by entity
* Optional visibility rules

### 🌐 Visibility Options

To support shared access between entities, each object may include one of the following fields:

* `"visibility": "public"` — object is readable by all authenticated users
* `"sharedWith": ["partner1", "partner2"]` — readable only by specified entities

Additionally, for fine-grained privacy, objects can include an optional `_privateFields` array to explicitly list which fields should be hidden from non-owners.

### 🔐 Explicit Redaction Metadata

This provides per-object control over field-level visibility:

```json
{
  "@type": "SensorReading",
  "value": 33.1,
  "entity": "acme",
  "sharedWith": ["regulatorX"],
  "_privateFields": ["entity", "sharedWith"]
}
```

If a user other than `acme` accesses the object, the response will omit the listed fields.

This system is simple now but can later evolve to use an ontology-based type system for automated redaction policies.

---

## 🧪 Curl Examples

### Create an object

```bash
curl -X POST http://localhost:2691/objects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"@type":"Test","value":123,"entity":"acme"}'
```

### Get all objects

```bash
curl http://localhost:2691/objects
```

### Get one object

```bash
curl http://localhost:2691/objects/urn:1r-micro:abc123
```

### Update an object

```bash
curl -X PUT http://localhost:2691/objects/urn:1r-micro:abc123 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"@type":"Test","value":456}'
```

### Delete an object

```bash
curl -X DELETE http://localhost:2691/objects/urn:1r-micro:abc123 \
  -H "Authorization: Bearer <token>"
```

### Render an object in Markdown

```bash
curl http://localhost:2691/objects/urn:1r-micro:abc123/render?format=md
```

### Subscribe to sensor readings

```bash
curl -X POST http://localhost:2691/subscriptions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"target": "http://client.example.com/webhook", "filter": {"@type": "SensorReading"}, "events": ["created"]}'
```

### Post a domain event

```bash
curl -X POST http://localhost:2691/events \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"@type":"Event","eventType":"arrivedAtGate","object":"urn:1r-micro:ULD456","timestamp":"2025-05-08T16:45:00Z"}'
```

---

## Notes

* All requests and responses are in JSON.
* The API is intended to be minimal, portable, and federated-ready.
