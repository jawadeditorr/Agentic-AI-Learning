 #agent creation will happen here
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from aws.ec2 import list_instances,get_instance_by_id,restart_instance,start_instance,stop_instance,terminating_instance
from langchain.chat_models import init_chat_model
from pprint import pprint

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
        terminating_instance
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
                "content":"list instances"
            }
        ]
    }
)

print(response["messages"][-1].content)