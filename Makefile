.PHONY: test lint check format install clean graph

graph:
	python3 scripts/build_graph.py

test:
	pytest tests/ -v

lint:
	ruff check src/ tests/

format:
	ruff format src/ tests/

check: lint test

install:
	pip install -e .

clean:
	rm -rf build dist *.egg-info .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
