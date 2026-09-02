"""Datastore creation and document ingestion helpers."""

import os
from typing import List, Tuple

import requests


def get_or_create_datastore(client, datastore_name: str) -> str:
    """Return the ID of an existing datastore with this name, creating one if needed."""
    datastores = client.datastores.list()
    existing_datastore = next((ds for ds in datastores if ds.name == datastore_name), None)

    if existing_datastore:
        print(f"Using existing datastore with ID: {existing_datastore.id}")
        return existing_datastore.id

    result = client.datastores.create(name=datastore_name)
    print(f"Created new datastore with ID: {result.id}")
    return result.id


def download_and_ingest_documents(
    client,
    datastore_id: str,
    files_to_upload: List[Tuple[str, str]],
    data_dir: str = "data",
) -> List[str]:
    """Download each file (if not already cached locally) and ingest it into the datastore."""
    os.makedirs(data_dir, exist_ok=True)

    document_ids = []
    for filename, url in files_to_upload:
        file_path = os.path.join(data_dir, filename)

        if not os.path.exists(file_path):
            print(f"Fetching {file_path}")
            try:
                response = requests.get(url)
                response.raise_for_status()
                with open(file_path, "wb") as f:
                    f.write(response.content)
            except Exception as e:
                print(f"Error downloading {filename}: {e}")
                continue

        try:
            with open(file_path, "rb") as f:
                ingestion_result = client.datastores.documents.ingest(datastore_id, file=f)
                document_ids.append(ingestion_result.id)
                print(f"Successfully uploaded {filename} to datastore {datastore_id}")
        except Exception as e:
            print(f"Error uploading {filename}: {e}")

    print(f"Successfully uploaded {len(document_ids)} files to datastore")
    print(f"Document IDs: {document_ids}")
    return document_ids


def print_first_document_metadata(client, datastore_id: str, document_ids: List[str]) -> None:
    if not document_ids:
        print("No documents were ingested; skipping metadata lookup.")
        return

    metadata = client.datastores.documents.metadata(
        datastore_id=datastore_id, document_id=document_ids[0]
    )
    print("Document metadata:", metadata)
