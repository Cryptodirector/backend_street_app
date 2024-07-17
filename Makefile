.PHONY: format

format:
	ruff check .


fastapi:
	fastapi dev main.py


migrate:
	alembic revision --autogenerate -m ''
	alembic upgrade head