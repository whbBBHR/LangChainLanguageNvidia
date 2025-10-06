"""
NVIDIA RAG LLM with LangChain Integration
This script demonstrates how to use NVIDIA AI endpoints with LangChain
for Retrieval-Augmented Generation (RAG) applications.
"""

import os
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA

# Load environment variables from .env file
load_dotenv()

def main():
    """
    Main function to demonstrate NVIDIA AI endpoints with LangChain
    """
    # Get API key from environment variable
    nvidia_api_key = os.getenv("NVIDIA_API_KEY")
    
    if not nvidia_api_key:
        raise ValueError(
            "NVIDIA_API_KEY not found in environment variables. "
            "Please set it in your .env file or environment."
        )
    
    # Initialize NVIDIA Chat model
    llm = ChatNVIDIA(
        model="meta/llama-3.1-8b-instruct",
        api_key=nvidia_api_key,
        temperature=0.7,
        max_tokens=1024,
    )
    
    print("NVIDIA RAG LLM initialized successfully!")
    print(f"Using model: meta/llama-3.1-8b-instruct")
    print("-" * 50)
    
    # Example usage
    prompt = "What is LangChain and how does it help in building AI applications?"
    
    print(f"\nPrompt: {prompt}\n")
    print("Response:")
    
    # Invoke the model
    response = llm.invoke(prompt)
    print(response.content)
    print("-" * 50)
    
    return response

if __name__ == "__main__":
    main()
