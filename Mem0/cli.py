"""Interactive REPL for the research assistant."""

import config
from assistant import PersonalResearchAssistant


def interactive_demo(assistant: PersonalResearchAssistant) -> None:
    print("\nType a research question, 'memories' to list what's been learned, or 'quit' to exit.")
    while True:
        try:
            question = input("\nYou: ")

            if question.lower() in ("quit", "exit", "q"):
                print("\nThanks for trying the Research Assistant!")
                break
            elif question.lower() == "memories":
                memories = assistant.get_memories(user_id=config.DEFAULT_USER_ID)
                if memories:
                    print("\nHere's what I've learned about your research interests:")
                    for i, memory in enumerate(memories, 1):
                        print(f"{i}. {memory}")
                else:
                    print("\nNo memories yet. Start asking about your research interests!")
            elif question.strip():
                answer = assistant.ask(question, user_id=config.DEFAULT_USER_ID)
                print(f"\nAssistant: {answer}")

        except KeyboardInterrupt:
            print("\n\nDemo ended. Thanks for trying the Research Assistant!")
            break
        except Exception as e:
            print(f"\nError: {e}")
