# Description

This is a command line tool that facilitates data enrichment of any Elasticsearch index.

It was originally designed to enrich BODS v0.4 data, but it actually
facilitates the enrichment of any Elasticsearch index.

It needs one "source" index, containing the data to be enriched, and one or more
different indices containing the additional data to be added to the source.

In order to keep this flexible, a configuration file is used to map the fields
that will be enriched, the enrichment data source for each field, and the
fields that will be used to match the documents in the source index with the
documents in the enrich index.

The first enricher use case is to add additional identifiers to BODS data,
using the LEI as the key to match the documents. The additional identifiers
will be sourced from OpenCorporates data.

Relevant documentation:
- [Elasticsearch ingest enrichment](https://www.elastic.co/guide/en/elasticsearch/reference/current/ingest-enriching-data.html)
- [Enrich processor](https://www.elastic.co/guide/en/elasticsearch/reference/current/enrich-processor.html)


# Enrichment concepts

In Elasticsearch enrichment, `match_field`, `enrich_field`, and `target_field` are crucial parameters that define how data from a source index is added to documents in a target index.

- `match_field`: This field specifies which field in the source index should be used to find matching documents.
  Elasticsearch compares the value of this field in the source index with a corresponding field in the incoming document
  to determine if there is a match.
- `enrich_field`: This parameter specifies the field from the source index that will be added to the target document.
  It contains the enrich data from the source indices that you want to add to incoming documents.
- `target_field`: This parameter specifies the name of the field that will be added to the incoming document. The
  matched enrich_field's value will be added to this target_field in the target document. This target field will contain
  the matched and enrichment fields specified in the enrich policy.


## Installation

This tool is written in Python, and can be installed using `uv`:

```bash
uv sync --frozen
```

Alternatively, you may use the bundled shell script:

```bash
./bin/install
```

# Usage

The tool can be run using the following command:

```bash
uv run enricher
```

The tool will look for a configuration file in the current directory, named
`config.yaml`.

## Commands

### `config`

This command is a small utility to manage the configuration file.

```bash
# get: retrieve a value from the configuration file
uv run python -m enricher config get <key>
# Example:
uv run python -m enricher config get source.index

# set: set a value in the configuration file
uv run python -m enricher config set <key> <value>
# Example:
uv run python -m enricher config set source.index entity

# set: remove a key from the configuration file
uv run python -m enricher config set <key>
# Example:
uv run python -m enricher config set source.index
```

### `enrich`

This command is used to set up and start the enrichment process.

```bash
# setup: set up the enrichment processor(s) configured
uv run python -m enricher enrich setup

# start: start the enrichment process.
uv run python -m enricher enrich start
```

## Configuration

This utility is configured via a YAML file, named `config.yaml` by default.
There are two main sections in the configuration file: `source` and `enrichment`.
Multiple enrichment policies can be defined in the `enrichment` section, each with its own set of parameters.

The `source` section contains the configuration for the source index, which is the index that will be enriched.
The `enrichments` section contains the configuration for the enrichment indices, which are the indices that will be used
to enrich the source index.

The configuration file should contain the following keys:

- `source.index`: the name of the Elasticsearch index containing the data to be enriched.
- `source.host`: the full URI of the Elasticsearch instance.
- `enrichments`:
  - `name`: the name of the enrichment policy (e.g. `add_oc_ids`).
  - `index`: the name of the Elasticsearch index containing the enrichment data.
  - `match_field`: the field in the source index that will be used to match documents.
  - `enrich_field`: the field in the enrichment index that will be added to the source index.
  - `target_field`: the field in the target index that will be used to store the enriched data.



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
docker-compose run --rm enricher config get source.host
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
