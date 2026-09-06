"""Scripted demo conversation and memory analysis for the research assistant."""

from typing import List

import config
from assistant import PersonalResearchAssistant

DEMO_QUESTIONS = [
    "I prefer papers that include practical implementation details and code examples. "
    "Theoretical papers without code are less useful for my work.",
    "What about BERT and GPT models? Are they related to my research interests?",
    "Actually, I also need to understand the theoretical foundations of attention mechanisms. "
    "Can you recommend some foundational theory papers?",
]

SEMANTIC_SEARCH_TEST_QUERIES = [
    "neural networks",  # should connect to transformers
    "code implementations",  # should find practical preferences
    "attention mechanisms",  # should connect to transformer interest
    "deep learning papers",  # should find research interests
]


def run_demo_conversation(assistant: PersonalResearchAssistant) -> None:
    for question in DEMO_QUESTIONS:
        answer = assistant.ask(question, user_id=config.DEFAULT_USER_ID)
        print(f"\nYou: {question}")
        print(f"Assistant: {answer}")


def analyze_extracted_memories(assistant: PersonalResearchAssistant) -> List[str]:
    print("\nMEMORY ANALYSIS - what did the assistant learn?")
    print("=" * 60)

    all_memories = assistant.get_memories(user_id=config.DEFAULT_USER_ID)

    if not all_memories:
        print("\nNo memories found. Run the demo conversation first.")
        return []

    print(f"\nTotal memories extracted: {len(all_memories)}")
    print("\nKey insights Mem0 learned about you:")
    for i, memory in enumerate(all_memories, 1):
        print(f"{i}. {memory}")

    print("\nTesting semantic search capabilities:")
    for query in SEMANTIC_SEARCH_TEST_QUERIES:
        related = assistant.search_memories(query, user_id=config.DEFAULT_USER_ID)
        print(f"\nQuery: '{query}'")
        print(f"Found {len(related)} related memories")
        if related:
            print(f"Top match: {related[0][:100]}...")

    return all_memories
