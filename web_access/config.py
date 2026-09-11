"""Configuration for the hybrid web + vector-search research agent.

Combines live Tavily web search/crawl/extract with a local Chroma vector
store over internal CRM notes, reasoned over by an OpenAI chat model.
"""

import os

from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CHAT_MODEL = os.environ.get("CHAT_MODEL", "gpt-4.1")

# Ingestion (ingest.py): source PDFs and chunking parameters.
DOCS_DIR = os.environ.get("DOCS_DIR", "./docs")
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Shared Chroma vector store (vector_store.py), populated by ingest.py and
# queried by the agent's vector_search tool.
VECTOR_DB_DIR = os.environ.get("VECTOR_DB_DIR", "supplemental/db")
VECTOR_COLLECTION_NAME = os.environ.get("VECTOR_COLLECTION_NAME", "crm")
