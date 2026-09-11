"""Chroma vector store shared by the ingestion script (ingest.py) and the
hybrid agent's vector_search tool (tools.py)."""

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

import config


def get_vector_store() -> Chroma:
    return Chroma(
        collection_name=config.VECTOR_COLLECTION_NAME,
        embedding_function=OpenAIEmbeddings(api_key=config.OPENAI_API_KEY),
        persist_directory=config.VECTOR_DB_DIR,
    )


def get_retriever():
    return get_vector_store().as_retriever()
