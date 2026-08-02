 #agent creation will happen here
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key

model = GoogleGenerativeAI(model="gemini-2.5-flash")

response=model.invoke("What is AWS?")
print(response)
