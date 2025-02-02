# Description

This is a command line tool that facilitates data enrichment of a GLEIF
Elasticsearch index.

It needs an index containing the output of our GLEIF pipeline, and one or more
different indices containing the additional data to be added to the GLEIF index.

In order to keep this flexible, a configuration file is used to map the fields
that will be enriched, the enrichment data source for each field, and the
fields that will be used to match the documents in the GLEIF index with the
documents in the enrich index.

The first iteration will aim to add additional identifiers to GLEIF data,
using the LEI as the key to match the documents. The additional identifiers
will be sourced from OpenCorporates data.

Relevant documentation:
- [Elasticsearch ingest enrichment](https://www.elastic.co/guide/en/elasticsearch/reference/current/ingest-enriching-data.html)
- [Enrich processor](https://www.elastic.co/guide/en/elasticsearch/reference/current/enrich-processor.html)

## Installation

This tool is written in Python, and can be installed using `uv`:

```bash
uv sync
```

Alternatively, you may use the bundled shell script:

```bash
./bin/install
```

# Usage

The tool can be run using the following command:

```bash
uv run gleif-enricher
```

The tool will look for a configuration file in the current directory, named
`config.yaml`.

## Commands

### `config`

```bash
# get: retrieve a value from the configuration file
uv run python -m gleif_enricher config get <key>
# Example:
uv run python -m gleif_enricher config get source.index

# set: set a value in the configuration file
uv run python -m gleif_enricher config set <key> <value>
# Example:
uv run python -m gleif_enricher config set source.index gleif_index_name

# set: remove a key from the configuration file
uv run python -m gleif_enricher config set <key>
# Example:
uv run python -m gleif_enricher config set source.index
```

### `enrich`


```bash
# setup: set up the enrichment processor(s) configured
uv run python -m gleif_enricher enrich setup

# start: start the enrichment process.
uv run python -m gleif_enricher enrich start
```

## Docker

This tool can be run using Docker and Docker Compose.

Building:

```bash
docker-compose build enricher
```

Running:
```bash
docker-compose run --rm enricher
docker-compose run --rm enricher <command>
# Examples
docker-compose run --rm enricher config get source.es.host
docker-compose run --rm enricher enrich start
```


# Development

To run the tests, use the following command:

```bash
uv run pytest
```

To run the linter, use the following command:

```bash
uv run flake8
```

To run the formatter, use the following command:

```bash
uv run black .
```

# License

This project is licensed under the GNU Affero General Public License v3.0.
