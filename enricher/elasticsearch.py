from enricher.cli.config import get_value as cli_get


def setup_enrichment_oc_id(es):
    # Define the enrich policy
    enrich_policy = {
        "match": {
            "indices": cli_get(key="enrichment.es.index"),
            "match_field": cli_get(key="enrichment.match_field"),
            "enrich_fields": ["_id"],
        }
    }

    # Create and execute the enrich policy
    es.enrich.put_policy(
        name="add_oc_ids_policy",
        body=enrich_policy,
    )
    es.enrich.execute_policy(name="add_oc_ids_policy")

    # Define the enrich processor
    enrich_processor = {
        "description": "Add OpenCorporates ID to the document",
        "processors": [
            {
                "enrich": {
                    "policy_name": "add_oc_ids_policy",
                    "field": cli_get(key="enrichment.match_field"),
                    "target_field": "opencorporates_id",
                    "max_matches": "1",
                }
            }
        ],
    }

    # Create the ingest pipeline with the enrich processor
    es.ingest.put_pipeline(id="enrich_pipeline_oc_id", body=enrich_processor)


def setup_enrichment_national_ids(es):
    enrich_policy = {
        "match": {
            "indices": cli_get(key="enrichment.es.index"),
            "match_field": cli_get(key="enrichment.match_field"),
            "enrich_fields": ["_source.uid", "_source.jurisdiction_code"],
        }
    }

    # Create and execute the enrich policy
    es.enrich.put_policy(name="add_national_ids_policy", body=enrich_policy)
    es.enrich.execute_policy(name="add_national_ids_policy")

    # Define the enrich processor
    enrich_processor = {
        "description": "Add OpenCorporates ID to the document",
        "processors": [
            {
                "enrich": {
                    "policy_name": "add_national_ids_policy",
                    "field": cli_get(key="enrichment.match_field"),
                    "target_field": "national_id",
                    "max_matches": "1",
                }
            }
        ],
    }

    # Create the ingest pipeline with the enrich processor
    es.ingest.put_pipeline(id="enrich_pipeline_national_id", body=enrich_processor)
