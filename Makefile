SHELL := /bin/sh

UV := uv
PY := $(UV) run python

.PHONY: run sync build validate cns core clean

# Canonical entry point: dependency sync, full clean build, and validation.
run: sync
	$(PY) scripts/build_docs.py --clean
	$(MAKE) validate

sync:
	$(UV) sync

build: sync
	$(PY) scripts/build_docs.py --clean

validate:
	$(PY) -c 'import json; from pathlib import Path; path = Path("generated/index.json"); data = json.loads(path.read_text(encoding="utf-8")); sources = data.get("sources", []); assert sources, "generated/index.json has no sources"; assert all(item.get("sections") for item in sources), "a source has no split sections"; print(f"validated {len(sources)} sources")'

cns: sync
	$(PY) scripts/build_docs.py --only cns --clean

core: sync
	$(PY) scripts/build_docs.py --only cns,sctrls,trigger --clean

clean:
	rm -rf generated
