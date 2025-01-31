def setup_enrichment(es):
    # Define the enrich policy
    enrich_policy = {
        "match": {
            "indices": cli_get("enrichment.es.index"),
            "match_field": cli_get("enrichment.match_field"),
            "enrich_fields": ["additional_id"],
        }
    }

    # Create and execute the enrich policy
    es.enrich.put_policy(name="add_ids_policy", body=enrich_policy)
    es.enrich.execute_policy(name="add_ids_policy")

    # Define the enrich processor
    enrich_processor = {
        "description": "Enrich GLEIF data with additional IDs",
        "processors": [
            {
                "enrich": {
                    "policy_name": "add_ids_policy",
                    "field": "LEI",
                    "target_field": "enriched_data",
                    "max_matches": "1",
                }
            }
        ],
    }

    # Create the ingest pipeline with the enrich processor
    es.ingest.put_pipeline(id="enrich_pipeline", body=enrich_processor)


def create_ingest_pipeline(es):
    # Create the ingest pipeline with the enrich processor
    es.ingest.put_pipeline(id="enrich_pipeline", body=enrich_processor)
