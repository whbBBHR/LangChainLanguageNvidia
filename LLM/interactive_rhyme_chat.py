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
ChatNVIDIA.get_available_models()

## Simple Chat Pipeline
chat_llm = ChatNVIDIA(model="meta/llama-3.3-70b-instruct")

prompt = ChatPromptTemplate.from_messages([
    ("system", "Only respond in rhymes"),
    ("user", "{input}")
])

rhyme_chain = prompt | chat_llm | StrOutputParser()

# Interactive user input loop
def chat_with_ai():
    print("🎵 Welcome to the Rhyming AI Chat! 🎵")
    print("Ask me anything and I'll respond in rhymes!")
    print("Type 'quit' or 'exit' to end the conversation.\n")
    
    while True:
        try:
            # Get user input
            user_question = input("You: ").strip()
            
            # Check if user wants to quit
            if user_question.lower() in ['quit', 'exit', 'bye']:
                print("🎵 Goodbye! Thanks for chatting in rhyme! 🎵")
                break
            
            # Skip empty inputs
            if not user_question:
                print("Please enter a question or type 'quit' to exit.")
                continue
            
            print("AI: ", end="", flush=True)
            # Get AI response
            response = rhyme_chain.invoke({"input": user_question})
            print(response)
            print()  # Add blank line for readability
            
        except KeyboardInterrupt:
            print("\n\n🎵 Goodbye! Thanks for chatting in rhyme! 🎵")
            break
        except Exception as e:
            error_text = str(e)
            if "403" in error_text or "Authorization failed" in error_text:
                print("Sorry, NVIDIA API authorization failed (403).")
                print("Check that NVIDIA_API_KEY in your project .env is valid, active, and not wrapped in extra quotes.")
                print("You may need to regenerate the key at https://build.nvidia.com/ and restart the terminal.")
            else:
                print(f"Sorry, an error occurred: {e}")
            print("Please try again or type 'quit' to exit.\n")

# Start the interactive chat
if __name__ == "__main__":
    chat_with_ai()