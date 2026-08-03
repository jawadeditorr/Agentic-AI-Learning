 #agent creation will happen here
import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from aws.ec2 import list_instances,get_instance_by_id,restart_instance
from langchain.chat_models import init_chat_model

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is missing from environment variables or .env file.")

groq_model=init_chat_model("groq:llama-3.3-70b-versatile")
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     temperature=0
# )

agent=create_agent(
    model=groq_model,
    tools=[list_instances,get_instance_by_id,restart_instance],
    system_prompt="You are an AI DevOps Assistant."
)

response=agent.invoke({"messages":[{"role":"user","content":"Restart instance abc123"}]})
print(response["messages"][-1].content)