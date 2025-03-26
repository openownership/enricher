import click
from elasticsearch import Elasticsearch, BadRequestError, NotFoundError
from enricher.elasticsearch import (
    setup_enrichment_oc_id,
    setup_enrichment_national_ids,
)
from enricher.cli.config import get_value as get_config_value

es = Elasticsearch(
    hosts=[get_config_value(key="source.es.host")],
    headers={"Content-Type": "application/json"},
)


@click.command()
def setup():
    try:
        setup_enrichment_oc_id(es)
        setup_enrichment_national_ids(es)
    except BadRequestError as e:
        if e.error == "resource_already_exists_exception":
            print("Enrich processor already set up.")
            return None
    print("Enrich processor set up successfully.")


@click.command()
def start():
    if get_config_value(key="source.replace") == "false":
        es.reindex(
            body={
                "source": {"index": get_config_value(key="source.es.index")},
                "dest": {"index": get_config_value(key="source.es.index") + "_copy"},
            }
        )

    es.enrich.execute_policy(name="add_oc_ids_policy", wait_for_completion=False)
    es.enrich.execute_policy(name="add_national_ids_policy", wait_for_completion=False)
    print("Enriching data...")

