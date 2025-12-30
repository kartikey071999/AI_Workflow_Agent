check:
	ruff check . --fix
	black --check .

format:
	black .