import click
from elasticsearch import Elasticsearch
from gleif_enricher.elasticsearch import setup_enrichment, create_ingest_pipeline
from gleif_enricher.cli.config import get as cli_get


@click.command()
def setup():
    es = Elasticsearch(hosts=[cli_get("source.es.host")])
    setup_enrichment(es)
    create_ingest_pipeline(es)
    print("Enrich processor set up successfully.")


@click.command()
def start():
    print("Enriching data...")
