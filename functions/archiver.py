import datetime
import azure.functions as func
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient
import json

COSMOS_URI = "<cosmos-uri>"
COSMOS_KEY = "<cosmos-key>"
DATABASE_NAME = "billing-db"
CONTAINER_NAME = "billing-records"

BLOB_CONN_STR = "<storage-conn-str>"
BLOB_CONTAINER = "billing-archive"

client = CosmosClient(COSMOS_URI, credential=COSMOS_KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)
blob_service = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
blob_container = blob_service.get_container_client(BLOB_CONTAINER)

def main(mytimer: func.TimerRequest) -> None:
    threshold = datetime.datetime.utcnow() - datetime.timedelta(days=90)
    query = f"SELECT * FROM c WHERE c.timestamp < '{threshold.isoformat()}'"
    old_records = container.query_items(query, enable_cross_partition_query=True)

    for record in old_records:
        record_id = record['id']
        blob_name = f"{record_id}.json"
        blob_container.upload_blob(blob_name, json.dumps(record), overwrite=True)
        container.delete_item(record_id, partition_key=record['partitionKey'])