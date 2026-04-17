import os
from dotenv import load_dotenv

# Load environment variables from project root .env file
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)

# Get API key from environment variable
nvidia_api_key = os.getenv("NVIDIA_API_KEY", "").strip().strip('"').strip("'")
if not nvidia_api_key:
    raise ValueError("Please set your NVIDIA API key in the .env file")

# Debug: print key info
print(f"API Key loaded: {nvidia_api_key[:10]}... (length: {len(nvidia_api_key)})")

os.environ["NVIDIA_API_KEY"] = nvidia_api_key

from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Check available models
print("\nTesting API connection and checking available models...")
try:
    available_models = ChatNVIDIA.get_available_models()
    print(f"✓ API connection successful! Found {len(available_models)} models")
    
    # Find available Llama and Mistral models
    llama_models = [m.id for m in available_models if 'llama' in m.id.lower()]
    mistral_models = [m.id for m in available_models if 'mistral' in m.id.lower()]
    
    print("\nAvailable Llama models:")
    for model in llama_models[:5]:
        print(f"  - {model}")
    
    print("\nAvailable Mistral models:")
    for model in mistral_models[:5]:
        print(f"  - {model}")
        
except Exception as e:
    print(f"✗ Error checking models: {e}")
    print("\nThis might indicate:")
    print("  1. Invalid or expired API key")
    print("  2. Network connectivity issues")
    print("  3. API service downtime")
    print("\nPlease verify your API key at: https://build.nvidia.com/")
    raise

## Simple Chat Pipeline - Finding a working model
# Test multiple free tier models to find one that works
test_models = [
    "meta/llama-3.1-8b-instruct",
    "mistralai/mistral-7b-instruct-v0.3",
    "nvidia/llama-3.1-nemotron-nano-8b-v1",
    "google/gemma-2-2b-it"
]

working_model = None
for model_name in test_models:
    try:
        print(f"\nTesting model: {model_name}")
        test_llm = ChatNVIDIA(model=model_name)
        # Try a simple test
        test_result = test_llm.invoke("Say 'hello' only")
        print(f"✓ {model_name} works!")
        working_model = model_name
        break
    except Exception as e:
        print(f"✗ {model_name} failed: {str(e)[:100]}")
        continue

if not working_model:
    print("\n❌ None of the tested models worked with your API key.")
    print("\nPossible solutions:")
    print("1. Visit https://build.nvidia.com/ and log in with your account")
    print("2. Generate a new API key if yours is expired")
    print("3. Check if your account has access to any models")
    print("4. Some models may require payment or special access")
    raise Exception("No working model found. Please check your API key access at https://build.nvidia.com/")

print(f"\n{'='*60}")
print(f"Using working model: {working_model}")
print(f"{'='*60}\n")

chat_llm = ChatNVIDIA(model=working_model)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Only respond in rhymes"),
    ("user", "{input}")
])

rhyme_chain = prompt | chat_llm | StrOutputParser()

## Simple execution with hardcoded question
print(rhyme_chain.invoke({"input" : "Tell me about birds!"}))