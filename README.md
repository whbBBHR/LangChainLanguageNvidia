# 🤖 AI Chat Application with Automatic Conversation Logging

**Advanced LangChain + NVIDIA AI Endpoints Integration**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-🦜🔗-green.svg)](https://langchain.com/)
[![NVIDIA AI](https://img.shields.io/badge/NVIDIA-AI%20Endpoints-76B900.svg)](https://build.nvidia.com/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-red.svg)](https://flask.palletsprojects.com/)

A sophisticated AI chat application featuring **dual interfaces** (CLI & Web), **automatic conversation logging**, and **accuracy-first responses** powered by NVIDIA's Llama 3.3 70B model through LangChain.

---

## 🌟 **Key Features**

### 🎯 **Dual Chat Interfaces**
- **CLI Interface** (`accurate_chat.py`) - Terminal-based chat with accuracy-first responses
- **Web Interface** (`web_app/app.py`) - Professional Flask web application at `localhost:5001`
- Both interfaces include **automatic conversation logging**

### 📝 **Comprehensive Logging System**
- **Automatic Session Tracking** - Every conversation gets a unique session ID
- **Timestamp Precision** - Millisecond-level accuracy for each exchange
- **Response Time Metrics** - Performance monitoring for each AI response  
- **JSON-Formatted Logs** - Structured data for easy analysis and searching
- **Privacy Protection** - Local storage only, excluded from version control

### 🎯 **Accuracy-First Design**
- **DEEPSEEK Bug Fixed** - Correctly counts 1 'D' in "DEEPSEEK" (not 3)
- **Systematic Letter Counting** - Spells out words before counting for precision
- **Factual Accuracy Priority** - Prioritizes correctness over creative responses

### 🔒 **Security & Privacy**
- **Environment Variables** - API keys secured in `.env` file
- **Git Protection** - Sensitive data excluded via comprehensive `.gitignore`
- **Local Logging** - Conversation data remains on your machine

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.9+
- NVIDIA AI API Key from [build.nvidia.com](https://build.nvidia.com/)
- Virtual environment (recommended)

### **Installation**

```bash
# Clone the repository
git clone https://github.com/whbBBHR/LangChainLanguageNvidia.git
cd LangChainLanguageNvidia

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install dependencies (uses pinned versions to avoid compatibility issues)
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your NVIDIA_API_KEY
```

### **Configuration**
Create a `.env` file in the project root:
```bash
# .env
NVIDIA_API_KEY=nvapi-your-actual-key-here
```

---

## 💬 **Usage**

> **⚠️ Important:** Always activate the virtual environment before running any scripts!
> ```bash
> source .venv/bin/activate  # macOS/Linux
> # .venv\Scripts\activate   # Windows
> ```

### **CLI Chat Interface**
```bash
# 1. Activate virtual environment (REQUIRED)
source .venv/bin/activate

# 2. Run the CLI chat
python LLM/accurate_chat.py
```
- Interactive terminal chat with automatic logging
- Type your questions and get accuracy-focused responses
- All conversations saved to `conversation_logs/`

### **Web Chat Interface**  
```bash
# 1. Activate virtual environment (REQUIRED)
source .venv/bin/activate

# 2. Start the web server
cd web_app
python app.py
```
- Open `http://localhost:5001` in your browser
- Professional chat interface with real-time responses
- Same logging capabilities as CLI version

### **View Conversation Logs**
```bash
# 1. Activate virtual environment (REQUIRED)
source .venv/bin/activate

# 2. View conversation logs
python view_conversations.py --recent    # Latest conversation
python view_conversations.py --stats     # Overall statistics  
python view_conversations.py --help      # All available options
```

---

## 🏗️ **Project Structure**

```
📦 LangChainLanguageNvidia/
├── 🐍 LLM/                           # Core Chat Applications
│   ├── accurate_chat.py              # ⭐ CLI Interface (Main)
│   ├── LANGChainExpressLan.py        # Original demo script
│   └── interactive_rhyme_chat.py     # Creative chat variant
│
├── 🌐 web_app/                       # Flask Web Interface  
│   ├── app.py                        # ⭐ Web Server (Main)
│   ├── templates/index.html          # Chat interface
│   └── static/styles.css             # Professional styling
│
├── 🔧 Core System                    
│   ├── conversation_logger.py        # ⭐ Logging Engine
│   ├── view_conversations.py         # ⭐ Log Viewer & Analytics
│   └── test_logging_simple.py        # Logging system tests
│
├── 📝 conversation_logs/             # 🔒 Live Logs (Git Ignored)
│   └── chat_YYYYMMDD_HHMMSS_*.json   # Auto-generated session logs
│
├── 📋 sample_logs/                   # Anonymous Demo Examples
│   ├── sample_chat_session.json      # Basic interactions
│   ├── python_programming_session.json
│   ├── accuracy_testing_session.json
│   └── ... (6 total example conversations)
│
├── 📚 Documentation/
│   ├── FILE_STRUCTURE.md             # Complete project breakdown
│   ├── DIRECTORY_TREE.md             # Visual file organization
│   ├── DOTENV_TROUBLESHOOTING.md     # Environment setup guide
│   └── SESSION_LOGS_SUMMARY.md       # Session analysis
│
└── ⚙️ Configuration
    ├── .env                          # 🔒 API Keys (Git Ignored)  
    ├── .gitignore                    # Privacy protection
    └── .venv/                        # 🔒 Virtual environment
```

---

## 🔧 **Core Components**

### **ConversationLogger Class**
```python
# Automatic conversation logging with session tracking
logger = ConversationLogger()
logger.log_conversation(user_input, ai_response, response_time)
logger.end_session()  # Generate session summary
```

### **Accuracy-First System Prompt**
```python
# Prioritizes factual correctness over creativity
system_prompt = """You are a helpful and accurate AI assistant. 
Your primary goal is to provide factually correct information..."""
```

### **Environment Variable Loading**
```python  
# Robust path resolution for .env files
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(env_path)
```

---

## 📊 **Logging Features**

### **Session Metadata**
- Unique session IDs for organization
- Start/end timestamps with duration tracking
- Total exchange counts and analytics

### **Exchange Details**  
- User input and AI response pairs
- Response time measurements in seconds
- Sequential exchange numbering
- Precise timestamp for each interaction

### **Privacy Protection**
- All logs stored locally in `conversation_logs/`
- Directory excluded from git via `.gitignore`
- No conversation data sent to remote repositories

### **Sample Log Structure**
```json
{
  "session_id": "abc123",
  "session_start": "2025-10-09T14:30:00.000000",
  "conversations": [
    {
      "timestamp": "2025-10-09T14:30:15.000000", 
      "user_input": "How many Ds are in DEEPSEEK?",
      "ai_response": "Let me spell out DEEPSEEK: D-E-E-P-S-E-E-K. I can see exactly 1 letter 'D' at the beginning.",
      "response_time_seconds": 1.2,
      "exchange_number": 1
    }
  ],
  "total_exchanges": 1,
  "session_duration_minutes": 5.5
}
```

---

## 🧪 **Testing & Validation**

### **Accuracy Testing**
```bash
# Test the famous DEEPSEEK counting bug fix
python LLM/test_deepseek.py

# Expected output: "1 D" (previously incorrectly said "3 Ds")
```

### **Logging System Tests** 
```bash
# Test automatic logging functionality
python test_logging_simple.py

# Verify logs are created and formatted correctly  
python view_conversations.py --stats
```

### **Integration Testing**
- CLI interface with logging integration
- Web interface with session management
- Environment variable loading from subdirectories
- Cross-platform compatibility (macOS, Linux, Windows)

---

## 🔍 **Key Improvements & Bug Fixes**

### **DEEPSEEK Accuracy Bug (FIXED)**
- **Problem:** AI incorrectly counted 3 'D's in "DEEPSEEK"  
- **Solution:** Implemented systematic letter-by-letter spelling approach
- **Result:** Now correctly identifies exactly 1 'D' in "DEEPSEEK"

### **Dotenv Persistence Issues (FIXED)**
- **Problem:** Environment variables not loading from subdirectories
- **Solution:** Explicit path resolution to parent `.env` file
- **Result:** Reliable API key loading regardless of execution directory

### **Conversation Data Loss (FIXED)**  
- **Problem:** No persistent conversation history
- **Solution:** Comprehensive automatic logging system
- **Result:** All conversations preserved with rich metadata

---

## 🛠️ **Advanced Usage**

### **Custom System Prompts**
Modify the system prompt in `accurate_chat.py` or `web_app/app.py` to customize AI behavior:

```python
system_prompt = """Your custom instructions here..."""
```

### **Log Analysis**
```python
# Custom log analysis
from view_conversations import analyze_conversations
stats = analyze_conversations("conversation_logs/")
print(f"Total sessions: {stats['sessions']}")
```

### **Web Interface Customization**
- Modify `web_app/templates/index.html` for UI changes
- Update `web_app/static/styles.css` for styling  
- Add new Flask routes in `web_app/app.py` for features

---

## 🔒 **Security Considerations**

### **API Key Protection**
- Never commit `.env` files to version control
- Use environment variables for all sensitive data
- Rotate API keys regularly

### **Conversation Privacy**
- All logs stored locally only
- No data transmitted to external services (except NVIDIA API for responses)
- Logs excluded from git via `.gitignore`

### **Sample Data**
- Anonymous examples in `sample_logs/` for demonstration
- No personal information in committed sample data
- Statistical summaries without sensitive content

---

## 🔧 **Troubleshooting**

### **Common Issues**

#### **ModuleNotFoundError: No module named 'dotenv' (or other packages)**
```bash
# Problem: Virtual environment not activated
# Solution: Always activate before running scripts
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Then run your script
python LLM/accurate_chat.py
```

#### **NVIDIA_API_KEY not found**
```bash
# Problem: .env file not loaded or API key not set
# Solution: Check your .env file exists and contains:
NVIDIA_API_KEY=nvapi-your-actual-key-here

# Verify it's in the project root directory
ls -la .env
```

#### **Permission denied or file not found**
```bash
# Problem: Running from wrong directory
# Solution: Always run from project root
cd "/path/to/Nividia_Building RAG Agents with LLMs"
source .venv/bin/activate
python LLM/accurate_chat.py
```

#### **Web interface won't start**
```bash
# Problem: Port already in use or packages missing
# Solution: 
1. Activate virtual environment first
2. Check if port 5001 is free: lsof -i :5001
3. Kill existing process if needed: kill [PID]
```

#### **Conversation logs not saving**
```bash
# Problem: Permission issues or directory doesn't exist
# Solution: Check conversation_logs directory exists
mkdir -p conversation_logs
chmod 755 conversation_logs
```

---

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)  
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 **License**

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 **Acknowledgments**

- **NVIDIA** for providing powerful AI endpoints
- **LangChain** for the excellent framework
- **Flask** for the web interface capabilities
- **Python-dotenv** for environment management

---

## 📞 **Support**

- 📚 Check the documentation in `/docs/` folder
- 🐛 Report issues via GitHub Issues
- 💬 Ask questions in GitHub Discussions
- 📧 Contact: [Your contact information]

---

**Built with ❤️ using LangChain, NVIDIA AI Endpoints, and Flask**