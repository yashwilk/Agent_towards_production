"""
Mem0 personal research assistant: self-improving memory that automatically
extracts insights, resolves conflicts, and evolves with each interaction.
Instead of just storing raw conversation history, Mem0 builds a knowledge
system that learns user preferences and provides contextual understanding.

Phase 1 (always on): vector memory via Qdrant Cloud.
Phase 2 (optional): adds graph memory via Neo4j when NEO4J_* env vars are set.
"""

import argparse

from assistant import PersonalResearchAssistant
from cli import interactive_demo
from demo import analyze_extracted_memories, run_demo_conversation
from memory_store import get_hybrid_memory, get_vector_memory


def main():
    parser = argparse.ArgumentParser(description="Mem0 personal research assistant")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Launch the interactive chat loop after the scripted demo",
    )
    args = parser.parse_args()

    memory = get_vector_memory()
    assistant = PersonalResearchAssistant(memory)

    run_demo_conversation(assistant)
    analyze_extracted_memories(assistant)

    hybrid_memory = get_hybrid_memory()
    if hybrid_memory is not None:
        assistant = PersonalResearchAssistant(hybrid_memory)
        print("\nEnhanced (vector + graph) assistant ready.")

    if args.interactive:
        interactive_demo(assistant)
    else:
        print("\nRun with --interactive to chat with the assistant directly.")


if __name__ == "__main__":
    main()
