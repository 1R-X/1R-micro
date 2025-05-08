Here is the updated **top-level architecture** for 1R-Micro, made implementation-agnostic and reflecting recent updates like events, subscriptions, access control, and federation:

---

# 1R-Micro Architecture

**1R-Micro** is a minimal, modular, and embeddable semantic object server. It powers the **1R-X ecosystem** by enabling the creation, storage, linking, querying, and federation of JSON-LD objects across decentralized systems.

---

## 🎯 Design Principles

* **Small and Simple**: Zero-dependency core, deployable anywhere — from cloud to edge.
* **Semantic-first**: Based on JSON-LD for meaningful, linkable data.
* **Federated**: Designed for multi-entity, multi-node topologies.
* **Composability**: Everything is modular — objects, events, subscriptions, access rules.
* **Hackable**: Ideal for research, prototyping, and edge deployment.

---

## 🧱 Core Modules

### 1. **Object Store**

* Stores semantic objects in flat files or pluggable backends (e.g., filesystem, SQLite, cloud)
* Each object is a self-contained JSON-LD document
* All objects have a unique `@id` and optional metadata: `entity`, `visibility`, `_privateFields`

### 2. **REST API**

* CRUD endpoints for objects: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`
* Event publishing: `POST /events`
* Subscription management: `POST`, `GET`, `DELETE /subscriptions`
* Token introspection: `GET /whoami`
* Render endpoint for human-readable formats

### 3. **Access Control & Visibility**

* Entity-based permissions via bearer token or headers
* Object-level visibility: `"public"` or `"sharedWith"`
* Field-level redaction using `_privateFields`
* Supports multi-tenant deployments or single-entity mode

### 4. **Event System**

* Domain events are JSON-LD objects linked to other resources
* Triggers pub-sub matching based on filters and event types
* Webhook delivery is built-in (with retry planned)

### 5. **Pub/Sub Engine**

* Lightweight publish/subscribe system
* Subscriptions can filter by object type, values, and event kinds
* Supports local webhook delivery and future federation hooks

---

## 🔗 Object Semantics

Objects in 1R-Micro are:

* **Typed** (`@type`) and contextualized (`@context`)
* **Globally Identifiable** via `@id` URNs
* **Linkable** to other objects (`linkedTo`, etc.)
* **Ownable** via the `entity` field

#### Example:

```json
{
  "@context": "https://onerecord.iata.org/ns/cargo",
  "@type": "Shipment",
  "@id": "urn:1r-micro:abc123",
  "origin": "JFK",
  "destination": "FRA",
  "entity": "airline-x",
  "visibility": "public"
}
```

---

## 🔁 Federation & Sync

* 1R-Micro instances are **autonomous nodes**
* Future federation protocols will support:

  * Discovery
  * Object sync (pull/push)
  * Pub-sub routing across servers
* Object URNs remain stable across nodes

---

## 🖥️ UI & Dev Tools

* Optional web UI (`/frontend`) for testing and exploration
* Postable webhooks to verify subscription delivery
* Command-line tools and SDKs (planned) in Python, TypeScript, Rust

---

## 🔮 Planned Extensions

* Ontology-driven rules and validation
* Object signatures and change history
* Subscription filtering by SPARQL-like queries
* Federation layer using ActivityPub or Linked Data Notifications
* Storage plugins (e.g., Git, S3, IPFS)

---

## 🧠 Philosophy

1R-Micro is not a platform. It’s a **semantic engine** that can be embedded into your stack or product — lightweight, transparent, and federation-ready.

> **Build small. Connect big. Federate meaningfully.**

