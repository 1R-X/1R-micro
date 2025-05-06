# 1R-Micro Architecture

**1R-Micro** is a minimal, modular, and embeddable semantic object server. It forms the core engine of the 1R-X ecosystem — enabling the creation, storage, linkage, and federation of JSON-LD objects across decentralized systems.

---

## 🎯 Design Goals

* **Simplicity**: Easy to run anywhere — no dependencies, no complex setup.
* **Extensibility**: Works across domains with custom object types and contexts.
* **Federation-first**: Nodes can operate independently or exchange data with peers.
* **Semantics over syntax**: Data objects have meaning, not just structure.
* **Edge-ready**: Can run on laptops, sensors, and low-resource devices.

---

## 🧱 Core Components

### 1. **Object Store**

* Flat file storage (`object_store/`) or pluggable backend
* Each object is a JSON-LD file with a unique `@id`
* CRUD operations via REST

### 2. **REST API** (Python Flask)

| Method | Endpoint        | Description                 |
| ------ | --------------- | --------------------------- |
| GET    | `/objects`      | List all objects            |
| GET    | `/objects/<id>` | Fetch object by ID          |
| POST   | `/objects`      | Create a new object         |
| PUT    | `/objects/<id>` | Update an object (optional) |
| DELETE | `/objects/<id>` | Delete an object (optional) |

### 3. **JSON-LD Model**

* Built on the [W3C JSON-LD standard](https://www.w3.org/TR/json-ld11/)
* Uses `@context`, `@type`, and `@id` to define objects
* Extensible with domain vocabularies (cargo, climate, health, etc.)

### 4. **Federation Module** *(planned)*

* Peer discovery
* Object replication and subscription
* Webhook-based notifications

### 5. **CLI & SDKs** *(planned)*

* CLI for local operations and scripting
* SDKs in TypeScript, Rust for apps, UIs, and sensors

---

## 🔄 Federation Model

Every 1R-Micro node is:

* **Autonomous**: Stores and serves its own objects
* **Interoperable**: Can pull or push objects to other nodes
* **Verifiable**: Object origins and changes are traceable

Nodes may sync:

* Periodically
* On-demand (via API)
* Via pub-sub hooks

---

## 🔗 Object Model

Objects in 1R-Micro:

* Always have a unique `@id`
* May link to other objects via `@id` references
* Use types and properties defined by their `@context`

### Example

```json
{
  "@context": "https://onerecord.iata.org/ns/cargo",
  "@type": "Shipment",
  "@id": "urn:1r-micro:abc123",
  "origin": "JFK",
  "destination": "FRA"
}
```

---

## 🧪 Runtime Behavior

* Objects are stored as-is in the object store
* Indexing (planned) will support efficient retrieval by type or relationship
* Data remains inspectable, transferable, and semantically rich

---

## 📈 Planned Extensions

* Event model (`/events`, pub-sub)
* Secure object signing & verification
* Typed query language (SPARQL-lite or JSON-Path)
* Frontend graph viewer (via `1r-ui`)
* Support for additional backends (e.g., SQLite, IPFS)

---

## 🧠 Why This Matters

The architecture of 1R-Micro is intentionally small, transparent, and adaptable. It’s not a platform — it’s a tool you can embed, fork, remix, or federate, bringing semantic clarity to local and global data flows alike.

**Build small. Connect big.**
