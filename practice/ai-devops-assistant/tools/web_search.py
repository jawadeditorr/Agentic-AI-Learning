#tool for web search
import os 
from dotenv import load_dotenv
from langchain_tavily import (
    TavilySearch,
    TavilyExtract,
    TavilyMap,
    TavilyCrawl,
    TavilyResearch,
    TavilyGetResearch
)

load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY")
if tavily_api_key is not None:
    os.environ["TAVILY_API_KEY"] = tavily_api_key

search_web = TavilySearch(
    max_results=5,
    search_depth="basic",
    topic="general"
)

extract_web = TavilyExtract(
    extract_depth="basic",
    include_images=True
)

map_web = TavilyMap()

crawl_web = TavilyCrawl()

research_web = TavilyResearch(
    model="auto",
    citation_format="numbered",
    stream=True,
)

get_research = TavilyGetResearch()