#agent creation will happen here
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from aws.ec2 import list_instances,get_instance_by_id,restart_instance,start_instance,stop_instance,terminating_instance
from tools.web_search import search_web,extract_web,map_web,crawl_web,research_web,get_research


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

agent=create_agent(
    model=llm,
    tools=[
        list_instances,
        get_instance_by_id,
        restart_instance,
        start_instance,
        stop_instance,
        terminating_instance,
        search_web,
        extract_web,
        map_web,
        crawl_web,
        research_web,
        get_research
        ],
    system_prompt=(
        BASE_DIR / "prompts" / "system_prompt.md"
    ).read_text(encoding="utf-8")
)

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