"""Configuration and constants for the IntellAgent education-bot evaluation demo."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INTELLAGENT_DIR = PROJECT_ROOT / "intellagent"

# The `simulator` package lives inside the cloned intellagent repo, not on the
# default path, so make it importable regardless of the current working directory.
sys.path.insert(0, str(INTELLAGENT_DIR))

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

AGENT_NAME = "my_education_agent"
AGENT_INPUT_DIR = f"examples/{AGENT_NAME}/input"
AGENT_PROMPT_PATH = f"{AGENT_INPUT_DIR}/wiki.md"
AGENT_CONFIG_PATH = "config/my_education_config.yml"
LLM_ENV_PATH = "config/llm_env.yml"

RESULTS_DIR = "./results/education"
DATASET_NAME = "data_1"
EXPERIMENT_NAME = "exp_1"

DASHBOARD_SCRIPT = "simulator/visualization/Simulator_Visualizer.py"
DASHBOARD_URL = "http://localhost:8501"

EDUCATION_PROMPT = """
# Educational Assistant Guidelines

You are an educational assistant designed to help students with their learning needs. Follow these guidelines:

## Core Responsibilities:
- Provide clear, accurate information on educational topics
- Explain complex concepts in simple terms
- Help with homework questions by guiding the student through the solution process
- Recommend learning resources when appropriate

## Policies:
1. **Do not solve problems directly** - Instead, provide guidance and hints
2. **Use age-appropriate language** - Adjust explanations based on the student's level
3. **Encourage critical thinking** - Ask follow-up questions that promote deeper understanding
4. **Be patient and supportive** - Create a positive learning environment
5. **Verify understanding** - Check if the student has understood the explanation

## Subject Areas:
- Mathematics (Basic arithmetic to advanced calculus)
- Science (Physics, Chemistry, Biology)
- Language Arts (Grammar, Writing, Literature)
- Social Studies (History, Geography, Civics)

Remember, your goal is to help students learn and grow, not just provide answers.
"""

OLLAMA_MODEL = "qwen2.5:7b"  # must support native tool-calling; pull with `ollama pull qwen2.5:7b`

SIMULATION_CONFIG = {
    "environment": {
        "prompt_path": AGENT_PROMPT_PATH,
    },
    # llm_intellagent overrides all framework LLMs (user sim, critique, policy extractor, etc.)
    "llm_intellagent": {
        "type": "ollama",
        "name": OLLAMA_MODEL,
    },
    # llm_chat overrides the chatbot being evaluated
    "llm_chat": {
        "type": "ollama",
        "name": OLLAMA_MODEL,
    },
    # Local models are slower than cloud APIs - fewer workers, longer timeouts.
    "description_generator": {
        "policies_config": {"num_workers": 1, "timeout": 120},
        "edge_config": {"num_workers": 1, "timeout": 120},
        "description_config": {"num_workers": 1, "timeout": 120},
        "refinement_config": {"num_workers": 1, "timeout": 120},
    },
    "event_generator": {
        "symbolic_enrichment_config": {"num_workers": 1, "timeout": 120},
        "symbolic_constraints_config": {"num_workers": 1, "timeout": 120},
        "event_graph": {"num_workers": 1, "timeout": 300},
    },
    "dialog_manager": {
        "num_workers": 1,
        "timeout": 3600,
        "cost_limit": 999,
    },
    "analysis": {
        "num_workers": 1,
        "timeout": 120,
    },
    "dataset": {
        "num_samples": 5,  # reduced from 10; local inference is much slower
        "cost_limit": 999,
    },
}
