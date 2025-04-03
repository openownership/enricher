import json
from elasticsearch import Elasticsearch, helpers

# Initialize the Elasticsearch client
es = Elasticsearch("http://localhost:9200", verify_certs=False)

# Load the JSON data from the file
with open("add_ids-01.json", "r") as file:
    data = json.load(file)

# Prepare the data for bulk indexing
# actions = [{"_index": "add_ids", "_id": item["LEI"], "_source": item} for item in data]
actions = [
    {"_index": "add_ids", "_id": item["_id"], "_source": item["_source"]}
    for item in data
]


# Perform the bulk indexing
helpers.bulk(es, actions)

print("Data indexed successfully")
