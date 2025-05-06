# 1R-Micro (Python) – Architecture

This document explains the internal architecture of the **Python-based reference implementation** of 1R-Micro, located in the `micro-python/` directory. It is a lightweight, file-based semantic object server built using Flask.

---

## 🧱 Components

### 1. `server.py`

The main Flask application that:

* Exposes REST endpoints for object creation, retrieval, and listing
* Manages file-based storage of JSON-LD objects
* Automatically assigns unique `@id` URNs to each new object

### 2. `object_store/`

* Local directory used to store JSON-LD objects
* Each object is saved as a `.json` file using a UUID as its filename
* Files are retrievable by ID via API

### 3. `requirements.txt`

Specifies Python dependencies (currently only Flask).

---

## 🔁 API Logic

### Endpoint: `POST /objects`

* Accepts a JSON-LD object
* Assigns a unique `@id` (if not provided)
* Stores the object in the `object_store/` folder
* Returns the stored object (with `@id`)

### Endpoint: `GET /objects`

* Lists all stored objects by reading all `.json` files in `object_store/`

### Endpoint: `GET /objects/<id>`

* Retrieves a specific object by ID (matching filename)

> Optional endpoints like `PUT` or `DELETE` can be added later for full CRUD.

---

## 🧠 Design Characteristics

* **Stateless server**: No database, uses local file system
* **Semantic-first**: Operates directly on JSON-LD objects with `@context`, `@type`, `@id`
* **Self-contained**: No external services required
* **Readable and hackable**: Minimal codebase, ideal for experimentation

---

## 🧪 Development Notes

* All logs print to stdout — ideal for development
* No object validation is enforced yet — schema validation can be added via `jsonschema` or `shacl`
* Object syncing, pub/sub, and signatures are **planned but not yet implemented**

---

## 🚀 Running Locally

```bash
cd micro-python
pip install -r requirements.txt
python server.py
```

Server runs at: `http://localhost:5000`

---

## 📦 Future Enhancements

* Optional backend storage (e.g., SQLite or remote object store)
* Signature verification and change tracking
* Peer-to-peer object sync
* CLI tools for managing the object store

---

**This Python implementation serves as the reference point for all 1R-Micro language ports.**

Maintained by the 1R-X project.
