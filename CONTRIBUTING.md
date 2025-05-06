# Contributing to 1R-Micro

Welcome! We're excited that you're interested in contributing to **1R-Micro**, the core engine of the 1R-X project. Whether you're fixing bugs, improving documentation, writing code, or proposing ideas — you're helping shape the future of open, semantic, federated data.

---

## 👇 Where to Start

### 1. Clone the Repo

```bash
git clone https://github.com/1r-x/1r-micro.git
cd 1r-micro/micro-python  # Start with Python version
```

### 2. Run Locally

```bash
pip install -r requirements.txt
python server.py
```

Test the API at [http://localhost:5000](http://localhost:5000).

### 3. Try a Change

* Add an object type
* Improve the object store logic
* Tweak an endpoint or add a new one

---

## 💡 Ways to Contribute

* 🐛 Report bugs (use [Issues](https://github.com/1r-x/1r-micro/issues))
* 🛠 Submit fixes or improvements via pull requests
* 📚 Improve documentation or write tutorials
* 🧪 Create and share new object types and JSON-LD examples
* 🌍 Build language SDKs (Rust, TS, Go, etc.)
* 🧱 Extend the federation logic, pub-sub, or peer sync
* 🎨 Design a UI for viewing objects and graphs

---

## 🧱 Project Structure

```
1r-micro/
├── micro-python/        ← Flask-based microserver
├── micro-rust/          ← (Planned)
├── micro-ts-sdk/        ← (Planned)
├── shared-schemas/      ← JSON-LD vocabularies
├── examples/            ← Sample objects to test with
```

---

## 🔀 Pull Requests

* Fork the repo
* Create a feature branch
* Make your changes
* Commit with a clear message
* Push and open a pull request

We’ll review, discuss, and hopefully merge it! 🧡

---

## 🧠 Design Principles

* **Simple over clever**
* **Semantically clear** over technically verbose
* **Modular and embeddable**
* **Decentralized by design**
* **Inclusive and domain-agnostic**

---

## 📜 License

By contributing, you agree that your contributions will be licensed under:

* Code: MIT License
* Docs + Schemas: Creative Commons BY 4.0

---

## 🙌 Thank You

We’re building 1R-Micro as the foundation for a smarter, more open, and more trustworthy data future. Your contributions make that possible.

**– The 1R-X Team**
