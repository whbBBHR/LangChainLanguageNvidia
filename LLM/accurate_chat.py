import os
import sys
import time
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conversation_logger import ConversationLogger

# Load environment variables from .env file (specify parent directory path)
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
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

## Accurate Chat Pipeline with RAG
# Available models:
# - "meta/llama-3.3-70b-instruct" (knowledge cutoff: mid-1990)
# - "meta/llama-3.1-405b-instruct" (larger model, similar cutoff)
# - "nvidia/llama-3.1-nemotron-70b-instruct" (NVIDIA tuned, mid-1990)
chat_llm = ChatNVIDIA(model="meta/llama-3.3-70b-instruct")

# Initialize web search tool for RAG
search_wrapper = DuckDuckGoSearchAPIWrapper(max_results=3)
search_tool = DuckDuckGoSearchResults(api_wrapper=search_wrapper)

# Function to determine if a question needs web search
def needs_web_search(question: str) -> bool:
    """Determine if a question requires current/recent information"""
    current_indicators = [
        'current', 'latest', 'recent', 'today', 'now', 'this year', 'last year',
        '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999',
        '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009',
        '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019',
        '2020', '2021', '2022', '2023', '2024', '2025',
        'news', 'happening', 'what is', 'who is', 'when did',
        'price', 'stock', 'weather', 'score', 'winner', 'won', 'released', 'release',
        'new', 'update', 'version', 'announce', 'launch', 'president', 'election'
    ]
    question_lower = question.lower()
    return any(indicator in question_lower for indicator in current_indicators)

# Function to search the web for current information
def search_web(query: str) -> str:
    """Search the web and return relevant information"""
    try:
        print("🔍 Searching the web for current information...")
        results = search_tool.invoke(query)
        return results
    except Exception as e:
        return f"Web search unavailable: {str(e)}"

# RAG-enhanced prompt
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful and accurate AI assistant with access to current information up to December 2025.

You have two sources of knowledge:
1. Your base training data (cutoff: mid-2023)
2. Real-time web search results for current information (1990-2025)

When answering questions:
- If web search results are provided, prioritize them for questions about recent events or current information
- Use the search results to provide accurate, up-to-date answers about events from 2023 onwards
- If no web search results are available, answer normally WITHOUT mentioning any knowledge cutoff dates
- Do NOT mention "my knowledge cutoff is 2023" or similar phrases unless the user specifically asks about your training data
- Present information confidently based on what you know

For factual questions (like counting letters, math, dates, etc.), provide the correct answer first.

For counting letters in words:
1. First, spell out the word letter by letter
2. Count carefully 
3. Give the exact correct number

Always prioritize accuracy. When you have current web search results, use them confidently.

Current date: {current_date}"""),
    ("user", "{input}\n\nWeb Search Results (if available):\n{context}")
])

accurate_chain = rag_prompt | chat_llm | StrOutputParser()

# Interactive user input loop with accuracy focus
def accurate_chat():
    # Initialize conversation logger
    logger = ConversationLogger()
    
    print("🎯 Welcome to the RAG-Enhanced Accurate AI Chat! 🎯")
    print("Ask me anything - I have knowledge up to December 2025!")
    print(f"📝 Session ID: {logger.session_id}")
    print(f"📅 Current date: {datetime.now().strftime('%B %d, %Y')}")
    print("🔍 I'll automatically search the web for questions about recent events (2023-2025)!")
    print("Type 'quit' or 'exit' to end the conversation.\n")
    
    while True:
        try:
            # Get user input
            user_question = input("You: ").strip()
            
            # Check if user wants to quit
            if user_question.lower() in ['quit', 'exit', 'bye']:
                print("🎯 Goodbye! Thanks for the accurate conversation! 🎯")
                logger.end_session()
                summary = logger.get_session_summary()
                print(f"📊 Session Summary: {summary['exchanges']} exchanges in {summary['duration']:.1f} minutes")
                break
            
            # Skip empty inputs
            if not user_question:
                print("Please enter a question or type 'quit' to exit.")
                continue
            
            # Determine if web search is needed
            context = ""
            if needs_web_search(user_question):
                context = search_web(user_question)
            else:
                context = "No additional web search needed for this query."
            
            print("AI: ", end="", flush=True)
            # Get AI response with RAG and time it - streaming for real-time output
            start_time = time.time()
            response_chunks = []
            
            # Stream the response in real-time
            for chunk in accurate_chain.stream({
                "input": user_question,
                "context": context,
                "current_date": datetime.now().strftime('%B %d, %Y')
            }):
                print(chunk, end="", flush=True)
                response_chunks.append(chunk)
            
            response_time = time.time() - start_time
            response = "".join(response_chunks)
            
            print()  # New line after response
            print()  # Add blank line for readability
            
            # Log the conversation
            logger.log_conversation(user_question, response, response_time)
            
        except KeyboardInterrupt:
            print("\n\n🎯 Goodbye! Thanks for the accurate conversation! 🎯")
            logger.end_session()
            summary = logger.get_session_summary()
            print(f"📊 Session Summary: {summary['exchanges']} exchanges in {summary['duration']:.1f} minutes")
            break
        except Exception as e:
            print(f"Sorry, an error occurred: {e}")
            print("Please try again or type 'quit' to exit.\n")

# Start the accurate chat
if __name__ == "__main__":
    accurate_chat()