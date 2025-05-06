# 1R-Micro

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

```bash
# Clone the repo
git clone https://github.com/1r-x/1r-micro.git
cd 1r-micro/micro-python

# Create a virtual environment (optional)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python server.py
```

---

## 🔁 API Endpoints

| Method | Endpoint        | Description           |
| ------ | --------------- | --------------------- |
| GET    | `/`             | Health check          |
| GET    | `/objects`      | List all objects      |
| POST   | `/objects`      | Create a new object   |
| GET    | `/objects/<id>` | Get a specific object |

Objects are stored as JSON-LD and use `@id` for unique URIs.

---

## 🧪 Example

```bash
curl -X POST http://localhost:5000/objects \
  -H "Content-Type: application/json" \
  -d '{
    "@context": "https://onerecord.iata.org/ns/cargo",
    "@type": "Shipment",
    "shipmentID": "SHP123",
    "origin": "JFK",
    "destination": "FRA"
  }'
```

---

## 🧩 Extend It

* Add domain-specific object types and vocabularies
* Use peer sync modules for federation
* Embed into edge apps, IoT devices, or mobile apps
* Build a viewer using the 1R-UI

---

## 📄 License

* Code: [MIT License](LICENSE)
* Documentation and contexts: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

---

## 🌱 Contributing

We're building a modular, federated standard for the future of semantic data. Join us.

* GitHub: [github.com/1r-x](https://github.com/1r-x)
* Chat: Coming soon (Matrix or Discord)
* Docs: [`/docs`](../docs)

---

**Made with purpose by the 1R-X community.**
