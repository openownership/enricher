import click
from elasticsearch import Elasticsearch, BadRequestError, NotFoundError
from enricher.elasticsearch import (
    setup_enrichments,
    reset_enrichments,
    start_enrichments,
)
from enricher.cli.config import get_value as get_config_value

es = Elasticsearch(
    hosts=[get_config_value(key="source.host")],
    headers={"Content-Type": "application/json"},
    verify_certs=False,
)


@click.command()
def setup():
    try:
        setup_enrichments(es)
        print("Enrich processor set up successfully.")
    except BadRequestError as e:
        print("Error setting up enrich processor:", e)

@click.command()
def reset():
    try:
        reset_enrichments(es)
        print("Enrich processor reset successfully.")
    except BadRequestError as e:
        print("Error resetting enrich processor:", e)

@click.command()
def start():
    print("Enriching data...")
    start_enrichments(es)
    print("Enrichments completed successfully.")
