check:
	ruff check src/
	black --check src/

format:
	black src/
