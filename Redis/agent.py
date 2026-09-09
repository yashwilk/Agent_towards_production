"""The travel agent: a LangGraph agent with a two-tier memory system.

Short-term memory (the conversation itself) is persisted by the compiled
graph's Redis checkpointer, scoped to a thread_id.

Long-term memory (durable facts/preferences across conversations) is a RedisVL
vector index the agent searches automatically before responding (retrieve_memories),
and can also read from / write to itself mid-conversation via tool calls.
"""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from redisvl.index import SearchIndex

import config
from long_term_memory import add_memory, search_memories
from models import MemoryType

SYSTEM_PROMPT = (
    "You are a helpful travel agent. Use 'retrieve_memories_tool' if you need to "
    "recall something about this traveler that isn't already in the context below, "
    "and use 'store_memory_tool' whenever they share a durable preference or fact "
    "worth remembering for future trips."
)

SUMMARY_PROMPT = (
    "Summarize this conversation in one or two sentences, focusing on any travel "
    "preferences or plans the traveler mentioned."
)


def build_agent(memory_index: SearchIndex, checkpointer):
    llm = ChatOllama(model=config.OLLAMA_MODEL, base_url=config.OLLAMA_BASE_URL, temperature=0.2)

    @tool
    def store_memory_tool(content: str, memory_type: str = "semantic") -> str:
        """Store a durable fact or preference about the traveler for future conversations."""
        add_memory(memory_index, content, MemoryType(memory_type))
        return f"Stored memory: {content}"

    @tool
    def retrieve_memories_tool(query: str) -> str:
        """Search long-term memory for facts or preferences relevant to the query."""
        results = search_memories(memory_index, query)
        if not results:
            return "No relevant memories found."
        return "\n".join(f"- {r['content']}" for r in results)

    tools = [store_memory_tool, retrieve_memories_tool]
    llm_with_tools = llm.bind_tools(tools)

    def retrieve_memories(state: MessagesState) -> dict:
        last_human = next(
            (m for m in reversed(state["messages"]) if isinstance(m, HumanMessage)), None
        )
        if last_human is None:
            return {}

        results = search_memories(memory_index, last_human.content)
        if not results:
            return {}

        context = "\n".join(f"- {r['content']}" for r in results)
        return {
            "messages": [
                SystemMessage(content=f"Relevant memories about this traveler:\n{context}")
            ]
        }

    def respond(state: MessagesState) -> dict:
        response = llm_with_tools.invoke([SystemMessage(content=SYSTEM_PROMPT)] + state["messages"])
        return {"messages": [response]}

    def summarize_conversation(state: MessagesState) -> dict:
        summary = llm.invoke(state["messages"] + [HumanMessage(content=SUMMARY_PROMPT)])
        add_memory(memory_index, summary.content, MemoryType.EPISODIC)
        return {}

    graph = StateGraph(MessagesState)
    graph.add_node("retrieve_memories", retrieve_memories)
    graph.add_node("respond", respond)
    graph.add_node("tools", ToolNode(tools))
    graph.add_node("summarize_conversation", summarize_conversation)

    graph.add_edge(START, "retrieve_memories")
    graph.add_edge("retrieve_memories", "respond")
    graph.add_conditional_edges(
        "respond", tools_condition, {"tools": "tools", "__end__": "summarize_conversation"}
    )
    graph.add_edge("tools", "respond")
    graph.add_edge("summarize_conversation", END)

    return graph.compile(checkpointer=checkpointer)
