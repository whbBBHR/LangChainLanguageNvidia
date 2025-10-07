# Chat Session Logs

This directory contains sample conversation logs that demonstrate the logging system functionality.

## Log Structure

Each conversation log contains:
- **Session metadata**: ID, timestamps, duration
- **Individual exchanges**: User input, AI response, timing
- **Analytics data**: Response times, exchange counts

## Privacy Note

Actual conversation logs are stored in `conversation_logs/` directory which is excluded from version control for privacy protection.

## Sample Log Format

```json
{
  "session_id": "unique_session_id",
  "session_start": "ISO_timestamp",
  "session_end": "ISO_timestamp", 
  "log_version": "1.0",
  "conversations": [
    {
      "timestamp": "ISO_timestamp",
      "user_input": "User question",
      "ai_response": "AI response",
      "response_time_seconds": 0.8,
      "exchange_number": 1
    }
  ],
  "total_exchanges": 4,
  "session_duration_minutes": 5.5
}
```

## Usage

View logs using the conversation viewer:
```bash
python view_conversations.py --recent
python view_conversations.py --stats
```