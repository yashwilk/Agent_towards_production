"""The personal research assistant: an OpenAI chat completion backed by Mem0 memory."""

from typing import List

from openai import OpenAI

import config

SYSTEM_MESSAGE = (
    "You are a personal AI Research Assistant. Help users with research questions, "
    "remember their interests, and provide contextual recommendations."
)


class PersonalResearchAssistant:
    def __init__(self, memory_instance):
        self.client = OpenAI()
        self.memory = memory_instance
        print("Research Assistant initialized with Mem0 memory.")

    def ask(self, question: str, user_id: str = config.DEFAULT_USER_ID) -> str:
        previous_memories = self.search_memories(question, user_id=user_id)

        if previous_memories:
            memory_context = ", ".join(previous_memories)
            prompt = f"{SYSTEM_MESSAGE}\n\nUser input: {question}\nPrevious memories: {memory_context}"
        else:
            prompt = f"{SYSTEM_MESSAGE}\n\nUser input: {question}"

        try:
            response = self.client.chat.completions.create(
                model=config.LLM_MODEL,
                messages=[{"role": "system", "content": prompt}],
                temperature=0.1,
                max_tokens=2000,
            )
            answer = response.choices[0].message.content

            self.memory.add(question, user_id=user_id, metadata={"category": "research"})

            return answer
        except Exception as e:
            return f"Encountered an error: {e}"

    def get_memories(self, user_id: str) -> List[str]:
        try:
            memories = self.memory.get_all(user_id=user_id)
            return _extract_memory_text(memories)
        except Exception as e:
            print(f"Error retrieving memories: {e}")
            return []

    def search_memories(self, query: str, user_id: str) -> List[str]:
        try:
            memories = self.memory.search(query, user_id=user_id)
            return _extract_memory_text(memories)
        except Exception as e:
            print(f"Error searching memories: {e}")
            return []


def _extract_memory_text(memories) -> List[str]:
    if isinstance(memories, dict) and "results" in memories:
        return [m["memory"] for m in memories["results"]]
    if isinstance(memories, list):
        return [m["memory"] for m in memories]
    return []
