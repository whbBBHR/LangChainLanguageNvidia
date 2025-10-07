#!/usr/bin/env python3
"""
Conversation Log Viewer
View and analyze saved conversation logs
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
import argparse

def list_log_files(log_directory="conversation_logs"):
    """List all available log files"""
    log_dir = Path(log_directory)
    if not log_dir.exists():
        print(f"❌ Log directory '{log_directory}' not found")
        return []
    
    log_files = list(log_dir.glob("chat_*.json"))
    log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)  # Most recent first
    
    return log_files

def display_session_summary(log_file):
    """Display a summary of a session"""
    try:
        with open(log_file, 'r') as f:
            data = json.load(f)
        
        print(f"\n📋 Session Summary: {log_file.name}")
        print("=" * 50)
        print(f"Session ID: {data.get('session_id', 'Unknown')}")
        print(f"Start Time: {data.get('session_start', 'Unknown')}")
        print(f"End Time: {data.get('session_end', 'In Progress')}")
        print(f"Duration: {data.get('session_duration_minutes', 'N/A')} minutes")
        print(f"Total Exchanges: {data.get('total_exchanges', len(data.get('conversations', [])))}")
        
        if 'conversations' in data and data['conversations']:
            print(f"\nFirst Question: {data['conversations'][0]['user_input'][:100]}...")
            if len(data['conversations']) > 1:
                print(f"Last Question: {data['conversations'][-1]['user_input'][:100]}...")
        
    except Exception as e:
        print(f"❌ Error reading {log_file}: {e}")

def display_full_conversation(log_file):
    """Display the full conversation from a log file"""
    try:
        with open(log_file, 'r') as f:
            data = json.load(f)
        
        print(f"\n💬 Full Conversation: {log_file.name}")
        print("=" * 50)
        
        conversations = data.get('conversations', [])
        for i, conv in enumerate(conversations, 1):
            timestamp = datetime.fromisoformat(conv['timestamp']).strftime("%H:%M:%S")
            response_time = conv.get('response_time_seconds', 0)
            
            print(f"\n[{i}] {timestamp} (⏱️ {response_time:.2f}s)")
            print(f"👤 User: {conv['user_input']}")
            print(f"🤖 AI: {conv['ai_response']}")
            print("-" * 50)
            
    except Exception as e:
        print(f"❌ Error reading {log_file}: {e}")

def search_conversations(query, log_directory="conversation_logs"):
    """Search for conversations containing specific text"""
    log_files = list_log_files(log_directory)
    results = []
    
    print(f"🔍 Searching for: '{query}'")
    
    for log_file in log_files:
        try:
            with open(log_file, 'r') as f:
                data = json.load(f)
            
            conversations = data.get('conversations', [])
            for conv in conversations:
                if (query.lower() in conv['user_input'].lower() or 
                    query.lower() in conv['ai_response'].lower()):
                    results.append({
                        'file': log_file.name,
                        'session_id': data.get('session_id'),
                        'timestamp': conv['timestamp'],
                        'user_input': conv['user_input'],
                        'ai_response': conv['ai_response'][:200] + "..." if len(conv['ai_response']) > 200 else conv['ai_response']
                    })
                    
        except Exception as e:
            print(f"❌ Error searching {log_file}: {e}")
    
    return results

def main():
    parser = argparse.ArgumentParser(description='Conversation Log Viewer')
    parser.add_argument('--list', action='store_true', help='List all log files')
    parser.add_argument('--summary', type=str, help='Show summary of specific log file')
    parser.add_argument('--view', type=str, help='View full conversation from log file')
    parser.add_argument('--search', type=str, help='Search conversations for text')
    parser.add_argument('--recent', action='store_true', help='Show most recent conversation')
    parser.add_argument('--stats', action='store_true', help='Show overall statistics')
    
    args = parser.parse_args()
    
    log_directory = "conversation_logs"
    
    if args.list:
        log_files = list_log_files(log_directory)
        print(f"\n📁 Available Log Files ({len(log_files)} total):")
        print("=" * 50)
        for i, log_file in enumerate(log_files, 1):
            mod_time = datetime.fromtimestamp(log_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            print(f"{i:2d}. {log_file.name} ({mod_time})")
    
    elif args.summary:
        log_path = Path(log_directory) / args.summary
        if log_path.exists():
            display_session_summary(log_path)
        else:
            print(f"❌ Log file '{args.summary}' not found")
    
    elif args.view:
        log_path = Path(log_directory) / args.view
        if log_path.exists():
            display_full_conversation(log_path)
        else:
            print(f"❌ Log file '{args.view}' not found")
    
    elif args.search:
        results = search_conversations(args.search, log_directory)
        print(f"\n🔍 Found {len(results)} matching conversations:")
        for i, result in enumerate(results, 1):
            print(f"\n[{i}] {result['file']} - {result['timestamp']}")
            print(f"👤 User: {result['user_input']}")
            print(f"🤖 AI: {result['ai_response']}")
            print("-" * 50)
    
    elif args.recent:
        log_files = list_log_files(log_directory)
        if log_files:
            display_full_conversation(log_files[0])
        else:
            print("❌ No log files found")
    
    elif args.stats:
        log_files = list_log_files(log_directory)
        total_sessions = len(log_files)
        total_exchanges = 0
        total_duration = 0
        
        for log_file in log_files:
            try:
                with open(log_file, 'r') as f:
                    data = json.load(f)
                total_exchanges += data.get('total_exchanges', 0)
                total_duration += data.get('session_duration_minutes', 0)
            except:
                pass
        
        print(f"\n📊 Conversation Statistics:")
        print("=" * 30)
        print(f"Total Sessions: {total_sessions}")
        print(f"Total Exchanges: {total_exchanges}")
        print(f"Total Duration: {total_duration:.1f} minutes")
        if total_sessions > 0:
            print(f"Average Exchanges per Session: {total_exchanges/total_sessions:.1f}")
            print(f"Average Session Duration: {total_duration/total_sessions:.1f} minutes")
    
    else:
        # Default: show recent logs
        log_files = list_log_files(log_directory)
        if log_files:
            print(f"\n📝 Recent Conversation Logs ({len(log_files)} total):")
            print("=" * 50)
            for i, log_file in enumerate(log_files[:5], 1):  # Show 5 most recent
                display_session_summary(log_file)
                if i < 5 and i < len(log_files):
                    print("\n" + "─" * 50)
        else:
            print("❌ No conversation logs found")
        
        print(f"\nℹ️  Use --help for more options")

if __name__ == "__main__":
    main()