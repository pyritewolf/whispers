# Build backend
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8 AS backend

RUN pip install poetry
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false && poetry install

WORKDIR /app
