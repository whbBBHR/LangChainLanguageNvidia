import os
import sys
import time
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS

# Add the parent directory to the path so we can import from LLM folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conversation_logger import ConversationLogger
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

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Required for sessions
CORS(app)  # Enable CORS for all routes

# Global logger storage (in production, use proper session management)
user_loggers = {}

## Set up the Accurate Chat Pipeline
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

@app.route('/')
def index():
    """Serve the main chat interface"""
    # Initialize logger for new session
    if 'session_id' not in session:
        logger = ConversationLogger()
        session['session_id'] = logger.session_id
        user_loggers[logger.session_id] = logger
        print(f"🔄 New web session started: {logger.session_id}")
    
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_ai():
    """Handle AI chat requests"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        # Get or create logger for this session
        session_id = session.get('session_id')
        if session_id not in user_loggers:
            logger = ConversationLogger()
            session['session_id'] = logger.session_id
            user_loggers[logger.session_id] = logger
            session_id = logger.session_id
        
        logger = user_loggers[session_id]
        
        # Get AI response using the accurate chain and time it
        start_time = time.time()
        response = accurate_chain.invoke({"input": question})
        response_time = time.time() - start_time
        
        # Log the conversation
        logger.log_conversation(question, response, response_time)
        
        return jsonify({
            'answer': response,
            'session_id': session_id,
            'response_time': round(response_time, 2)
        })
    
    except Exception as e:
        print(f"Error in ask_ai: {e}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500

@app.route('/session-info')
def session_info():
    """Get current session information"""
    session_id = session.get('session_id')
    if session_id and session_id in user_loggers:
        logger = user_loggers[session_id]
        summary = logger.get_session_summary()
        return jsonify(summary)
    else:
        return jsonify({'error': 'No active session'}), 404

if __name__ == '__main__':
    print("🎯 Starting Accurate AI Chat Web Server...")
    print("📱 Open your browser to: http://localhost:5001")
    print("📝 Conversation logging enabled")
    app.run(debug=True, host='0.0.0.0', port=5001)