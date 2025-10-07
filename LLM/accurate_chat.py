import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
nvidia_api_key = os.getenv("NVIDIA_API_KEY")
if not nvidia_api_key:
    raise ValueError("Please set your NVIDIA API key in the .env file")

os.environ["NVIDIA_API_KEY"] = nvidia_api_key

from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

## Accurate Chat Pipeline
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

# Interactive user input loop with accuracy focus
def accurate_chat():
    print("🎯 Welcome to the Accurate AI Chat! 🎯")
    print("Ask me anything - I'll prioritize giving you correct answers!")
    print("Type 'quit' or 'exit' to end the conversation.\n")
    
    while True:
        try:
            # Get user input
            user_question = input("You: ").strip()
            
            # Check if user wants to quit
            if user_question.lower() in ['quit', 'exit', 'bye']:
                print("🎯 Goodbye! Thanks for the accurate conversation! 🎯")
                break
            
            # Skip empty inputs
            if not user_question:
                print("Please enter a question or type 'quit' to exit.")
                continue
            
            print("AI: ", end="", flush=True)
            # Get AI response with accuracy focus
            response = accurate_chain.invoke({"input": user_question})
            print(response)
            print()  # Add blank line for readability
            
        except KeyboardInterrupt:
            print("\n\n🎯 Goodbye! Thanks for the accurate conversation! 🎯")
            break
        except Exception as e:
            print(f"Sorry, an error occurred: {e}")
            print("Please try again or type 'quit' to exit.\n")

# Start the accurate chat
if __name__ == "__main__":
    accurate_chat()