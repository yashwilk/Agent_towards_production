"""Configuration for the Cognee-based AI memory system.

Loads .env so Cognee (which reads LLM_API_KEY / LLM_MODEL directly from the
environment) is configured, and centralizes the data paths and node-set names
shared across ingestion, search, and visualization.
"""

from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

GUIDO_CONTRIBUTIONS_FILE = DATA_DIR / "guido_contributions.json"
COPILOT_CONVERSATIONS_FILE = DATA_DIR / "copilot_conversations.json"
DEVELOPER_RULES_FILE = DATA_DIR / "my_developer_rules.md"
ZEN_PRINCIPLES_FILE = DATA_DIR / "zen_principles.md"
PEP_STYLE_GUIDE_FILE = DATA_DIR / "pep_style_guide.md"

# Node sets group ingested data so searches can be scoped to a domain.
GUIDO_NODE_SET = "guido_data"
DEVELOPER_NODE_SET = "developer_data"
PRINCIPLES_NODE_SET = "principles_data"

GRAPH_VISUALIZATION_PATH = BASE_DIR / "guido_contributions.html"
