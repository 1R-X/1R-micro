# 1R-Micro for Python

**A minimal, embeddable, federated object engine for semantic data exchange.**

1R-Micro is the core reference implementation of the 1R-X ecosystem — an open, lightweight, and extensible framework for creating, linking, and exchanging semantically meaningful objects across domains.

Whether you're building air cargo platforms, environmental sensor networks, digital twin systems, or scientific data logs, 1R-Micro gives you a portable, JSON-LD-native object store and REST API to model, share, and orchestrate real-world entities.

---

## ✨ Features

* 🧠 **JSON-LD native** semantic object modeling
* 🌍 **Federated-ready** — link and sync across nodes
* 🧱 **Zero-dependency backend** — just Python, file storage, and Flask
* 🚀 **Extensible** for any domain: cargo, science, media, climate
* 📡 **Offline-first** — runs on laptops, edge devices, even mobile
* 🔗 **Object linking** using URIs and `@id` references

---

## 📦 Installation

Absolutely. Here's a concise **"Developer Sandbox Setup"** section you can append to your `README.md` or `status.md` file to help contributors get started with running and testing 1R-Micro locally:

---

## 🧪 Developer Sandbox Setup

This section helps developers set up a local environment to explore, test, and extend 1R-Micro with full federation and event simulation.

---

### ✅ Requirements

* Python 3.10+
* `pip` and `venv`
* Optional: `make`, Docker, Postman or `curl`

---

### 📦 Setup Steps

```bash
# Clone the repo
git clone https://github.com/your-org/1r-micro.git
cd 1r-micro/micro-python

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### ▶️ Run the Server

```bash
python server.py
```

Server will start at:
`http://localhost:2691`

---

### 🌐 Open the Frontend

Visit:

```
http://localhost:2691/frontend
```

Use this embedded test app to:

* Create objects
* Send events
* Subscribe to webhooks
* View output and object graphs

---

### 🧪 Simulated Authentication

Use the `Authorization` header to simulate an entity:

```bash
-H "Authorization: Bearer acme"
```

This will set your entity to `acme` for the request.

---

### 🧲 Trigger Webhooks

You can run a **local webhook listener** with:

```bash
curl -X POST http://localhost:2691/v1/subscriptions \
  -H "Authorization: Bearer acme" \
  -H "Content-Type: application/json" \
  -d '{
        "target": "http://localhost:2691/webhook",
        "filter": { "@type": "Test" },
        "events": ["created"]
      }'
```

Then create a matching object to trigger the webhook.


