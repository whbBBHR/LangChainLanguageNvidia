#!/usr/bin/env python3
"""
Test Conversation Logging
Quick demo of the logging functionality
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from conversation_logger import ConversationLogger
import time

def demo_logging():
    print("🎯 Testing Conversation Logging System")
    print("=" * 40)
    
    # Create logger
    logger = ConversationLogger()
    print(f"📝 Session ID: {logger.session_id}")
    print(f"📁 Log file: {logger.log_file}")
    
    # Simulate some conversations
    conversations = [
        ("Hello, how are you?", "I'm doing great! How can I help you today?"),
        ("How many Ds are in DEEPSEEK?", "Let me spell it out: D-E-E-P-S-E-E-K. There is 1 D in DEEPSEEK."),
        ("What's the weather like?", "I don't have access to real-time weather data, but I can help with other questions!"),
        ("Thank you!", "You're welcome! Feel free to ask anything else.")
    ]
    
    for i, (user_input, ai_response) in enumerate(conversations, 1):
        print(f"\n[{i}] Logging conversation...")
        print(f"👤 User: {user_input}")
        print(f"🤖 AI: {ai_response}")
        
        # Simulate response time
        response_time = 0.5 + (i * 0.3)  # Varying response times
        logger.log_conversation(user_input, ai_response, response_time)
        
        time.sleep(0.5)  # Brief pause between conversations
    
    # End session
    print(f"\n📊 Ending session...")
    logger.end_session()
    
    # Show session summary
    summary = logger.get_session_summary()
    print(f"\n✅ Demo complete!")
    print(f"📋 Final summary: {summary}")

if __name__ == "__main__":
    demo_logging()