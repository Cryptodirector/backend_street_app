#
FROM python:3.11

#
WORKDIR /app

#
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev # Установка без зависимостей для разработки

COPY . .

CMD ["fastapi", "run", "main.py", "--proxy-headers", "--port", "8000"]