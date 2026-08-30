"""LangGraph is a powerful framework by LangChain designed for creating stateful, multi-actor applications with LLMs. 

State Management: Maintain persistent state across interactions
Flexible Routing: Define complex flows between components
Persistence: Save and resume workflows
Visualization: See and understand your agent's structure
"""

import os
from pathlib import Path
from typing import TypedDict, List

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_core.runnables.graph import MermaidDrawMethod

load_dotenv()


# First, let's update our State to include sentiment
class State(TypedDict):
    text: str
    classification: str
    entities: List[str]
    summary: str
    sentiment: str


# Initialize our language model with temperature=0 for more deterministic outputs
llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)




def classification_node(state: State):
    '''Classify the text into one of the categories: News, Blog, Research, or Other'''
    prompt = PromptTemplate(
        input_variables=["text"],
        template="Classify the following text into one of the categories: News, Blog, Research, or Other.\n\nText:{text}\n\nCategory:"
    )
    message = HumanMessage(content=prompt.format(text=state["text"]))
    classification = llm.invoke([message]).content.strip()
    return {"classification": classification}




def entity_extraction_node(state: State):
    '''Extract all the entities (Person, Organization, Location) from the text'''
    prompt = PromptTemplate(
        input_variables=["text"],
        template="Extract all the entities (Person, Organization, Location) from the following text. Provide the result as a comma-separated list.\n\nText:{text}\n\nEntities:"
    )
    message = HumanMessage(content=prompt.format(text=state["text"]))
    entities = llm.invoke([message]).content.strip().split(", ")
    return {"entities": entities}



def summarization_node(state: State):
    '''Summarize the text in one short sentence'''
    prompt = PromptTemplate(
        input_variables=["text"],
        template="Summarize the following text in one short sentence.\n\nText:{text}\n\nSummary:"
    )
    message = HumanMessage(content=prompt.format(text=state["text"]))
    summary = llm.invoke([message]).content.strip()
    return {"summary": summary}

# Create our sentiment analysis node
def sentiment_node(state: State):
    '''Analyze the sentiment of the text: Positive, Negative, or Neutral'''
    prompt = PromptTemplate(
        input_variables=["text"],
        template="Analyze the sentiment of the following text. Is it Positive, Negative, or Neutral?\n\nText:{text}\n\nSentiment:"
    )
    message = HumanMessage(content=prompt.format(text=state["text"]))
    sentiment = llm.invoke([message]).content.strip()
    return {"sentiment": sentiment}


# Route after classification
def route_after_classification(state: State) -> str:
    category = state["classification"].lower() # e.g. "news", "Category: News", etc.
    return any(keyword in category for keyword in ["news", "research"])


    # Create our StateGraph
workflow = StateGraph(State)

# Add nodes to the graph
workflow.add_node("classification_node", classification_node)
workflow.add_node("entity_extraction", entity_extraction_node)
workflow.add_node("summarization", summarization_node)
workflow.add_node("sentiment_analysis", sentiment_node)

# Add edges to the graph
workflow.set_entry_point("classification_node")  # Set the entry point of the graph
workflow.add_conditional_edges("classification_node", route_after_classification, path_map={
    True: "entity_extraction",
    False: "summarization"
})
workflow.add_edge("entity_extraction", "summarization")
workflow.add_edge("summarization", "sentiment_analysis")
workflow.add_edge("sentiment_analysis", END)


# Compile the graph
app = workflow.compile()

# Save a visualization of our graph to disk and open it
try:
    graph_path = Path(__file__).parent / "graph.png"
    graph_path.write_bytes(
        app.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)
    )
    print(f"Graph saved to {graph_path}")
    os.startfile(graph_path)
except Exception as e:
    print(f"Error generating visualization: {e}")
    print("The graph structure is: classification_node -> entity_extraction -> summarization -> END")


    
sample_text = """
OpenAI has announced the GPT-4 model, which is a large multimodal model that exhibits human-level performance on various professional benchmarks. It is developed to improve the alignment and safety of AI systems.
Additionally, the model is designed to be more efficient and scalable than its predecessor, GPT-3. The GPT-4 model is expected to be released in the coming months and will be available to the public for research and development purposes.
"""

state_input = {"text": sample_text}
result = app.invoke(state_input)

print("Classification:", result["classification"])
print("\nEntities:", result["entities"])
print("\nSummary:", result["summary"])
print("\nSentiment:", result["sentiment"])
# Replace this with your own text to analyze
your_text = """
The recent advancements in quantum computing have opened new possibilities for cryptography and data security. 
Researchers at MIT and Google have demonstrated quantum algorithms that could potentially break current encryption methods.
However, they are also developing new quantum-resistant encryption techniques to protect data in the future.
"""

# Process the text through our pipeline
your_result = app.invoke({"text": your_text})

print("Classification:", your_result["classification"])
print("\nEntities:", your_result["entities"])
print("\nSummary:", your_result["summary"])
print("\nSentiment:", your_result["sentiment"])


test_text = """
OpenAI released the GPT-4 model with enhanced performance on academic and professional tasks. It's seen as a major breakthrough in alignment and reasoning capabilities.
"""

result = app.invoke({"text": test_text})

print("Classification:", result["classification"])
print("Entities:", result.get("entities", "Skipped"))
print("Summary:", result["summary"])
print("Sentiment:", result["sentiment"])



blog_text = """
Here's what I learned from a week of meditating in silence. No phones, no talking—just me, my breath, and some deep realizations.
"""

result = app.invoke({"text": blog_text})

print("Classification:", result["classification"])
print("Entities:", result.get("entities", "Skipped (not applicable)"))
print("Summary:", result["summary"])
print("Sentiment:", result["sentiment"])