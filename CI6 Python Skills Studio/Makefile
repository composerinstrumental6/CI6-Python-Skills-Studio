PYTHON := python3
VENV := .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python
PYTEST := $(VENV)/bin/pytest

.PHONY: setup run test clean

setup:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -r requirements.txt

run: setup
	$(PY) app.py

test: setup
	$(PYTEST) -q

clean:
	rm -rf $(VENV) __pycache__ .pytest_cache tests/__pycache__
