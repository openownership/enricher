FROM python:3.11-slim

WORKDIR /app

COPY . .

COPY --from=ghcr.io/astral-sh/uv:0.5.5 /uv /uvx /bin/
RUN /bin/uv sync --frozen

# Set the entrypoint to the CLI application
ENTRYPOINT ["uv", "run", "enricher"]
