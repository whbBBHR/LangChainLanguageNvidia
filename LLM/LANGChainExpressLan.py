import os
from dotenv import load_dotenv

# Load environment variables from .env file in the project root
# This works correctly whether the script is run from the LLM/ subdirectory
# or from the project root.
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)

# Get API key from environment variable
nvidia_api_key = os.getenv("NVIDIA_API_KEY")
if not nvidia_api_key:
    raise ValueError(
        f"NVIDIA_API_KEY not found. Please create a .env file at:\n"
        f"  {env_path}\n"
        f"with the line:  NVIDIA_API_KEY=nvapi-your-key-here\n"
        f"Get your key at https://build.nvidia.com/"
    )

os.environ["NVIDIA_API_KEY"] = nvidia_api_key

try:
    from langchain_nvidia_ai_endpoints import ChatNVIDIA
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
except ImportError as e:
    raise ImportError(
        f"Required package import failed: {e}\n"
        "Run: pip install -r requirements.txt --upgrade"
    ) from e

try:
    ChatNVIDIA.get_available_models()
except Exception:
    pass

## Simple Chat Pipeline
chat_llm = ChatNVIDIA(model="meta/llama-3.3-70b-instruct")

prompt = ChatPromptTemplate.from_messages([
    ("system", "Only respond in rhymes"),
    ("user", "{input}")
])

rhyme_chain = prompt | chat_llm | StrOutputParser()

## Simple execution with hardcoded question
print(rhyme_chain.invoke({"input" : "Tell me about birds!"}))