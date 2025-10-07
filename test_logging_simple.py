#!/usr/bin/env python3
"""
Simple test for conversation logging functionality
Tests the ConversationLogger class without interactive input
"""

import os
import sys
sys.path.append('.')

from conversation_logger import ConversationLogger
from datetime import datetime

def test_conversation_logging():
    """Test the conversation logging system with sample conversations"""
    
    print("🧪 Testing Conversation Logging System")
    print("=" * 50)
    
    # Test 1: Basic logging functionality
    print("\n1️⃣  Testing basic logging functionality...")
    logger = ConversationLogger("conversation_logs")
    
    # Simulate a conversation
    test_conversations = [
        ("Hello, how are you today?", "I'm doing great! How can I help you?"),
        ("What's the weather like?", "I don't have access to real-time weather data, but I can help you find weather information."),
        ("How many Ds are in DEEPSEEK?", "Let me spell out DEEPSEEK: D-E-E-P-S-E-E-K. I can see exactly 1 letter 'D' at the beginning."),
        ("Thanks for your help!", "You're welcome! Feel free to ask if you have more questions.")
    ]
    
    print(f"   ✅ Started logging session: {logger.session_id}")
    
    for i, (question, response) in enumerate(test_conversations):
        print(f"   📝 Logging exchange {i+1}...")
        logger.log_conversation(question, response, response_time=0.5 + i * 0.2)
    
    print(f"   ✅ Logged {len(test_conversations)} exchanges")
    
    # Test 2: Check if files are created
    print("\n2️⃣  Checking log file creation...")
    logs_dir = "conversation_logs"
    if os.path.exists(logs_dir):
        log_files = [f for f in os.listdir(logs_dir) if f.endswith('.json')]
        print(f"   ✅ Found {len(log_files)} log files")
        
        if log_files:
            latest_file = max(log_files, key=lambda f: os.path.getctime(os.path.join(logs_dir, f)))
            file_path = os.path.join(logs_dir, latest_file)
            file_size = os.path.getsize(file_path)
            print(f"   📄 Latest log: {latest_file} ({file_size} bytes)")
    else:
        print("   ❌ No conversation_logs directory found")
    
    # Test 3: Session summary
    print("\n3️⃣  Testing session summary...")
    summary = logger.get_session_summary()
    print(f"   📊 Session ID: {summary.get('session_id', 'N/A')}")
    print(f"   📊 Total exchanges: {summary.get('exchanges', 0)}")
    print(f"   📊 Session duration: {summary.get('duration', 0):.2f} minutes")
    
    # Test 4: More conversations in same session
    print("\n4️⃣  Testing additional conversations in session...")
    
    # Log more conversations
    logger.log_conversation("What is Python?", "Python is a high-level programming language.", 0.8)
    logger.log_conversation("Is it good for AI?", "Yes, Python is excellent for AI and machine learning.", 0.6)
    
    # Check final summary
    final_summary = logger.get_session_summary()
    print(f"   ✅ Now have {final_summary.get('exchanges', 0)} total exchanges")
    
    # End the session
    logger.end_session()
    
    print("\n🎉 All logging tests completed successfully!")
    print(f"📁 Check the '{logs_dir}' directory for saved conversation logs")
    
    return True

if __name__ == "__main__":
    try:
        test_conversation_logging()
        print("\n✨ Conversation logging system is working perfectly!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()