from elasticsearch import Elasticsearch
from cli import (
    get as cli_get,
)  # Import the get_nested function from the cli module

# Connect to Elasticsearch
es_source = Elasticsearch([cli_get("source.es.host")])
es_enrichment = Elasticsearch([cli_get("enrichment.es.host")])

# Define the enrich policy
enrich_policy = {
    "match": {
        "indices": cli_get("enrichment.es.index"),
        "match_field": cli_get("enrichment.match_field"),
        "enrich_fields": ["additional_id"],
    }
}

# Create the enrich policy
es_source.enrich.put_policy(name="add_ids_policy", body=enrich_policy)

# Execute the enrich policy to create the enrich index
es_source.enrich.execute_policy(name="add_ids_policy")

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
es_source.ingest.put_pipeline(id="enrich_pipeline", body=enrich_processor)

print("Enrich processor set up successfully.")
