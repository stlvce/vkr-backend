FROM python:3.11

RUN curl -sSL https://install.python-poetry.org | python -

WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . /app

CMD ["poetry", "run", "uvicorn", "app.main:app", "--reload", "0.0.0.0", "--port", "8000"]