#tool for web search
import os 
import json
import requests
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_tavily import TavilySearch

load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY")
if tavily_api_key is not None:
    os.environ["TAVILY_API_KEY"] = tavily_api_key

"""
tool = TavilySearch(
    max_results=5,
    topic="general",
    # include_answer=False,
    # include_raw_content=False,
    # include_images=False,
    # include_image_descriptions=False,
    # search_depth="basic",
    # time_range="day",
    # start_date=None,
    # end_date=None,
    # include_domains=None,
    # exclude_domains=None,
    # include_usage= False
)
"""

search_web = TavilySearch(
    max_results=5,
    topic="general"
)