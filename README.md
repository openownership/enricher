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

This tool is written in Python, and can be installed using poetry:

```bash
poetry install
```

# Usage

The tool can be run using the following command:

```bash
poetry run python -m gleif_enricher
```

The tool will look for a configuration file in the current directory, named
`config.yml`. Structure TBD.

The `gleif_index` field should contain the name of the Elasticsearch index
containing the GLEIF data.


# Development

To run the tests, use the following command:

```bash
poetry run pytest
```

To run the linter, use the following command:

```bash
poetry run flake8
```

To run the formatter, use the following command:

```bash
poetry run black .
```

# License

This project is licensed under the AGPL-3.0 License - see the [LICENSE](LICENSE).

