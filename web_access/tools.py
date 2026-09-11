"""Tool definitions for the hybrid agent: live web tools from Tavily plus a
retriever tool over the internal CRM vector store."""

from langchain_tavily import TavilyCrawl, TavilyExtract, TavilySearch

import config
from vector_store import get_retriever

web_search = TavilySearch(max_results=10, topic="general", tavily_api_key=config.TAVILY_API_KEY)
web_extract = TavilyExtract(extract_depth="advanced", tavily_api_key=config.TAVILY_API_KEY)
web_crawl = TavilyCrawl(tavily_api_key=config.TAVILY_API_KEY)

vector_search = get_retriever().as_tool(
    name="vector_search",
    description="Perform a vector search on our company's internal CRM data.",
)

ALL_TOOLS = [web_search, web_crawl, web_extract, vector_search]
