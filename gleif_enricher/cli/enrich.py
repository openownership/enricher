import click
from elasticsearch import Elasticsearch
from gleif_enricher.elasticsearch import (
    setup_enrichment_oc_id,
    setup_enrichment_national_ids,
)
from gleif_enricher.cli.config import get_value as cli_get

es = Elasticsearch(hosts=[cli_get(key="source.es.host")])


@click.command()
def setup():
    setup_enrichment_oc_id(es)
    setup_enrichment_national_ids(es)
    print("Enrich processor set up successfully.")


@click.command()
def start():
    es.enrich.execute_policy(name="add_oc_ids_policy", wait_for_completion=False)
    es.enrich.execute_policy(name="add_national_ids_policy", wait_for_completion=False)
    print("Enriching data...")
