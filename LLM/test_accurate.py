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

## Test the accurate version
chat_llm = ChatNVIDIA(model="meta/llama-3.3-70b-instruct")

# Improved prompt for accuracy
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful and accurate AI assistant. 

For factual questions (like counting letters, math, dates, etc.), provide the correct answer first, then be creative with your response style.

For counting letters in words:
1. First, spell out the word letter by letter
2. Count carefully 
3. Give the exact correct number
4. Then add any creative or rhyming elements if appropriate

Always prioritize accuracy over creativity for factual questions."""),
    ("user", "{input}")
])

accurate_chain = prompt | chat_llm | StrOutputParser()

# Test the DEEPSEEK question with improved accuracy
print("🎯 Testing Accurate Version:")
print("Question: How many Ds are in DEEPSEEK?")
print("Expected: 1 D (D-E-E-P-S-E-E-K)")
print("\nAI Response:")
response = accurate_chain.invoke({"input": "How many Ds are in DEEPSEEK?"})
print(response)