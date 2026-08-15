#agent creation will happen here
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from aws.ec2 import list_instances,get_instance_by_id,restart_instance,start_instance,stop_instance,terminating_instance
from aws.s3 import list_s3_buckets,create_s3_bucket,delete_s3_bucket,get_bucket_by_name
from tools.web_search import search_web,extract_web,map_web,crawl_web,research_web,get_research
from middleware.logging import logging_middleware
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage, SystemMessage


load_dotenv()

BASE_DIR=Path(__file__).parent

# groq_api_key = os.getenv("GROQ_API_KEY")
# if not groq_api_key:
#     raise ValueError("GROQ_API_KEY is missing from environment variables or .env file.")

# groq_model=init_chat_model("groq:llama-3.3-70b-versatile")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

checkpointer=InMemorySaver()

agent=create_agent(
    model=llm,
    tools=[
        #ec2 tools
        list_instances,
        get_instance_by_id,
        restart_instance,
        start_instance,
        stop_instance,
        terminating_instance,

        #s3 tools
        list_s3_buckets,
        create_s3_bucket,
        delete_s3_bucket,
        get_bucket_by_name,

        #web search tools
        search_web,
        extract_web,
        map_web,
        crawl_web,
        research_web,
        get_research
    ],

    #middlewares
    middleware=[
        logging_middleware,
        SummarizationMiddleware(
            model=llm,
            trigger=("tokens",5000),
            keep = ("tokens",3000)
        )
    ],

    #checkpoint of in memory saver
    checkpointer=checkpointer,

    #system prompt from the markdown file
    system_prompt=(
        BASE_DIR / "prompts" / "system_prompt.md"
    ).read_text(encoding="utf-8")
)

config = {"configurable": {"thread_id": "thread1"}}

response = agent.invoke(
    {
        "messages":[
            {
                "role":"user",
                "content":"What is DevOps?"
            }
        ]
    }
)

print(response["messages"][-1].content)