FROM python:3.11-slim

WORKDIR /app

# COPY pyproject.toml poetry.lock ./
COPY . .

RUN pip install poetry
RUN poetry install

# Set the entrypoint to the CLI application
ENTRYPOINT ["poetry", "run", "python", "gleif_enricher/cli.py"]