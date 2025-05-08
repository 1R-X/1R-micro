# Makefile for 1R-Micro

run:
	python server.py

install:
	pip install -r requirements.txt

test:
	pytest tests/

lint:
	black . --check

format:
	black .

reset:
	rm -rf object_store/*.json

whoami:
	curl http://localhost:2691/v1/whoami -H "Authorization: Bearer acme"

openapi:
	python scripts/gen_openapi.py > openapi.json

sync:
	python sync.py

frontend:
	open http://localhost:2691/frontend

