"""
Conversation Logging Utility
Automatically logs chat conversations with timestamps and session tracking
"""

import os
import json
import datetime
from pathlib import Path
import uuid

class ConversationLogger:
    def __init__(self, log_directory="conversation_logs"):
        """Initialize the conversation logger"""
        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(exist_ok=True)
        self.session_id = str(uuid.uuid4())[:8]  # Short session ID
        self.session_start = datetime.datetime.now()
        
        # Create session-specific log file
        timestamp = self.session_start.strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_directory / f"chat_{timestamp}_{self.session_id}.json"
        
        # Initialize log file with session info
        self._init_session_log()
    
    def _init_session_log(self):
        """Initialize the log file with session metadata"""
        session_info = {
            "session_id": self.session_id,
            "session_start": self.session_start.isoformat(),
            "log_version": "1.0",
            "conversations": []
        }
        
        with open(self.log_file, 'w') as f:
            json.dump(session_info, f, indent=2)
    
    def log_conversation(self, user_input, ai_response, response_time=None):
        """Log a single conversation exchange"""
        try:
            # Read existing log
            with open(self.log_file, 'r') as f:
                log_data = json.load(f)
            
            # Create conversation entry
            conversation_entry = {
                "timestamp": datetime.datetime.now().isoformat(),
                "user_input": user_input,
                "ai_response": ai_response,
                "response_time_seconds": response_time,
                "exchange_number": len(log_data["conversations"]) + 1
            }
            
            # Add to conversations
            log_data["conversations"].append(conversation_entry)
            log_data["last_updated"] = datetime.datetime.now().isoformat()
            log_data["total_exchanges"] = len(log_data["conversations"])
            
            # Write back to file
            with open(self.log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
                
            print(f"💾 Conversation logged to: {self.log_file.name}")
            
        except Exception as e:
            print(f"⚠️ Logging error: {e}")
    
    def end_session(self):
        """Mark the end of a chat session"""
        try:
            with open(self.log_file, 'r') as f:
                log_data = json.load(f)
            
            log_data["session_end"] = datetime.datetime.now().isoformat()
            session_duration = datetime.datetime.now() - self.session_start
            log_data["session_duration_minutes"] = round(session_duration.total_seconds() / 60, 2)
            
            with open(self.log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
                
            print(f"📊 Session ended. Duration: {log_data['session_duration_minutes']} minutes")
            print(f"📁 Full log saved: {self.log_file}")
            
        except Exception as e:
            print(f"⚠️ Session end logging error: {e}")
    
    def get_session_summary(self):
        """Get a summary of the current session"""
        try:
            with open(self.log_file, 'r') as f:
                log_data = json.load(f)
            
            return {
                "session_id": log_data.get("session_id"),
                "exchanges": log_data.get("total_exchanges", 0),
                "duration": (datetime.datetime.now() - self.session_start).total_seconds() / 60,
                "log_file": str(self.log_file)
            }
        except Exception as e:
            return {"error": str(e)}

def create_daily_summary(log_directory="conversation_logs"):
    """Create a daily summary of all conversations"""
    log_dir = Path(log_directory)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    summary = {
        "date": today,
        "total_sessions": 0,
        "total_exchanges": 0,
        "sessions": []
    }
    
    # Process all log files from today
    for log_file in log_dir.glob(f"chat_{datetime.datetime.now().strftime('%Y%m%d')}_*.json"):
        try:
            with open(log_file, 'r') as f:
                log_data = json.load(f)
            
            session_summary = {
                "session_id": log_data.get("session_id"),
                "start_time": log_data.get("session_start"),
                "end_time": log_data.get("session_end"),
                "exchanges": log_data.get("total_exchanges", 0),
                "duration_minutes": log_data.get("session_duration_minutes", 0)
            }
            
            summary["sessions"].append(session_summary)
            summary["total_sessions"] += 1
            summary["total_exchanges"] += session_summary["exchanges"]
            
        except Exception as e:
            print(f"Error processing {log_file}: {e}")
    
    # Save daily summary
    summary_file = log_dir / f"daily_summary_{today}.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    return summary, summary_file