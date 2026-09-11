"""Loads every PDF in config.DOCS_DIR, splits it into chunks, and persists the
chunks into the shared Chroma vector store (vector_store.py).

Run this once, or whenever the source documents change, before running main.py:
    python ingest.py
"""

import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config
from vector_store import get_vector_store


def load_documents(docs_dir: str) -> list:
    file_paths = [
        os.path.join(docs_dir, name)
        for name in os.listdir(docs_dir)
        if os.path.isfile(os.path.join(docs_dir, name))
    ]

    documents = []
    for file_path in file_paths:
        try:
            docs = PyPDFLoader(file_path=file_path).load()
            documents.extend(docs)
            print(f"Loaded {len(docs)} pages from {file_path}")
        except Exception as e:
            print(f"Error loading {file_path}: {e}")

    return documents


def main() -> None:
    documents = load_documents(config.DOCS_DIR)
    print(f"Loaded {len(documents)} document pages total")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")

    vector_store = get_vector_store()
    vector_store.add_documents(chunks)
    print(
        f"Persisted {len(chunks)} chunks to '{config.VECTOR_DB_DIR}' "
        f"(collection '{config.VECTOR_COLLECTION_NAME}')"
    )


if __name__ == "__main__":
    main()
