from elasticsearch import Elasticsearch, BadRequestError, NotFoundError
from collections import namedtuple
from enricher.cli.config import get_value as get_config_value, convert_to_namedtuple


def enrichment_name_to_policy_name(enrichment_name):
    """
    Convert the enrichment name to a policy name.
    """
    return f"{enrichment_name}_policy"


def enrichment_name_to_pipeline_name(enrichment_name):
    """
    Convert the enrichment name to a pipeline name.
    """
    return f"enrich_pipeline_{enrichment_name}"


def setup_enrichment(es: Elasticsearch, enrichment: namedtuple) -> None:
    """
    Set up the enrichment policy and processor in Elasticsearch.
    :param es: elasticsearch client
    :param enrichment: enrichment configuration
    :return: None
    """
    policy_name = enrichment_name_to_policy_name(enrichment.name)

    # Define the enrich policy
    enrich_policy = {
        "match": {
            "indices": enrichment.index,
            "match_field": enrichment.match_field,
            "enrich_fields": enrichment.enrich_fields,
        }
    }

    # Create and execute the enrich policy
    es.enrich.put_policy(
        name=policy_name,
        body=enrich_policy,
    )

    print('Creating enrich policy:', policy_name, end="... ")
    es.enrich.execute_policy(
        name=policy_name,
        wait_for_completion=False
    )
    print("done (running asynchronously).")


def make_enrichment_processor(es: Elasticsearch, enrichment: namedtuple) -> dict:
    """
    Set up the enrichment processor in Elasticsearch.
    :param es: elasticsearch client
    :param enrichment: enrichment configuration
    :return: None
    """

    # Define the enrich processor
    enrich_processor = {
        "enrich": {
            "policy_name": enrichment_name_to_policy_name(enrichment.name),
            "field": enrichment.match_field,
            "target_field": enrichment.target_field,
            "max_matches": "1",
            "ignore_failure": True,
        }
    }
    return enrich_processor


def setup_enrichments(es: Elasticsearch) -> None:
    enrichments = []

    for enrichment in get_config_value(key="enrichments"):
        enrichments.append(convert_to_namedtuple(enrichment))

    for enrichment in enrichments:
        try:
            setup_enrichment(es, enrichment)
        except BadRequestError as e:
            if e.error == "resource_already_exists_exception":
                print("Enrich processor already set up.")


def reset_enrichments(es: Elasticsearch) -> None:
    try:
        es.ingest.delete_pipeline(
            id="openownership_enrich_pipeline",
        )
        print("Enrich pipeline reset successfully.")
    except Exception as e:
        print(e)

    for enrichment in get_config_value(key="enrichments"):
        try:
            es.enrich.delete_policy(
                name=enrichment_name_to_policy_name(enrichment.get("name"))
            )
            print(f"Enrich policy {enrichment.get('name')} reset successfully.")
        except BadRequestError as e:
            if e.error == "resource_not_found_exception":
                print("Enrich policy not found.")
            else:
                print("Error resetting enrich policy:", e)
        except NotFoundError as e:
            print("Enrich policy not found:", e)


def start_enrichments(es: Elasticsearch) -> None:
    """
    Start the enrichment process for all configured enrichments.
    Also set up pipelines for each enrichment.
    :param es:
    :return:
    """
    enrichments = []
    for enrichment in get_config_value(key="enrichments"):
        enrichments.append(convert_to_namedtuple(enrichment))

    processors = []
    for enrichment in enrichments:
        processors.append(make_enrichment_processor(es, enrichment))

    for enrichment in enrichments:
        # Create the ingest pipeline with the enrich processor
        enrich_pipeline = {
            "description": "Pipeline for enriching BODS data",
            "processors": processors,
        }

        # import ipdb; ipdb.set_trace()

        es.ingest.put_pipeline(
            id="openownership_enrich_pipeline",
            body=enrich_pipeline,
        )

    for enrichment in enrichments:
        print("Starting enrichment for:", enrichment.name, end="... ")
        es.enrich.execute_policy(
            name=enrichment_name_to_policy_name(enrichment.name),
            wait_for_completion=False
        )
        print("done (running asynchronously).")
