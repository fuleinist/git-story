.PHONY: install test clean

install:
	pip install -e .

test:
	python -m pytest -v

clean:
	rm -rf build/ dist/ *.egg-info __pycache__ .pytest_cache
	find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true
