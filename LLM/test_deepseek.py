import os
from dotenv import load_dotenv

# Load environment variables from project root .env file
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)

# Get API key from environment variable
nvidia_api_key = os.getenv("NVIDIA_API_KEY", "").strip().strip('"').strip("'")
if not nvidia_api_key:
    raise ValueError("Please set your NVIDIA API key in the .env file")

os.environ["NVIDIA_API_KEY"] = nvidia_api_key

from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

## Simple Chat Pipeline
chat_llm = ChatNVIDIA(model="meta/llama-3.3-70b-instruct")

prompt = ChatPromptTemplate.from_messages([
    ("system", "Only respond in rhymes"),
    ("user", "{input}")
])

rhyme_chain = prompt | chat_llm | StrOutputParser()

# Test the DEEPSEEK question
print("Testing: How many Ds are in DEEPSEEK?")
print("Correct answer: 1 D")
print("\nAI Response:")
response = rhyme_chain.invoke({"input": "How many Ds are in DEEPSEEK?"})
print(response)