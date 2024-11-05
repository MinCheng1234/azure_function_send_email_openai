# blob_utils.py
import json
import os
import logging
from azure.storage.blob import BlobServiceClient

# Function to upload JSON to Blob Storage
def upload_to_blob(blob_name, content, BLOB_STORAGE_CONNECTION_STRING, OUTPUT_CONTAINER):
    from azure.storage.blob import BlobServiceClient

    blob_service_client = BlobServiceClient.from_connection_string(BLOB_STORAGE_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=OUTPUT_CONTAINER, blob=blob_name)
    
    # Upload content as a JSON string
    blob_client.upload_blob(json.dumps(content), overwrite=True)
    logging.info(f"Uploaded {blob_name} to Blob Storage.")