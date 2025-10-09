# 🔧 Dotenv Persistence Issues - Complete Guide

## ❌ **Why Dotenv Variables Don't Persist**

### **1. Path Resolution Problems (Most Common)**
```python
# ❌ WRONG - looks for .env in current working directory
load_dotenv()

# ✅ CORRECT - specify exact path to .env file
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)
```

### **2. Working Directory vs Script Location**
```bash
# When you run from project root
cd "/Users/wayneberry/Documents/Nividia_Building RAG Agents with LLMs"
python LLM/accurate_chat.py  # ✅ Works - .env found in cwd

# When you run from LLM directory  
cd LLM
python accurate_chat.py      # ❌ Fails - .env not in ./LLM/
```

### **3. Environment Variable Scope**
```python
# ❌ Variables only exist during script execution
load_dotenv()
# Script ends → variables disappear

# ✅ Variables persist in shell session
export NVIDIA_API_KEY="your-key-here"
# Available until terminal closes
```

---

## ✅ **Fixed Implementation (Already Applied)**

### **File: `LLM/accurate_chat.py`**
```python
# Load environment variables from .env file (specify parent directory path)
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)
```

### **File: `web_app/app.py`**
```python
# Load environment variables from .env file (specify parent directory path)  
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)
```

---

## 🧪 **Test the Fix**

### **1. Test CLI Application**
```bash
cd "/Users/wayneberry/Documents/Nividia_Building RAG Agents with LLMs"
source .venv/bin/activate
python LLM/accurate_chat.py
```

### **2. Test Web Application**  
```bash
cd "/Users/wayneberry/Documents/Nividia_Building RAG Agents with LLMs/web_app"
source .venv/bin/activate
python app.py
```

### **3. Verify Environment Loading**
```python
# Add this debug code temporarily
print(f"Environment file path: {env_path}")
print(f"File exists: {os.path.exists(env_path)}")
print(f"API Key loaded: {'Yes' if os.getenv('NVIDIA_API_KEY') else 'No'}")
```

---

## 🔍 **Common Dotenv Persistence Issues & Solutions**

### **Issue 1: Wrong Working Directory**
**Problem:** Running script from different directory than .env location
**Solution:** Use absolute path to .env file

### **Issue 2: Virtual Environment Not Activated**  
**Problem:** Packages not available, imports fail before dotenv loads
**Solution:** Always activate virtual environment first

### **Issue 3: Multiple .env Files**
**Problem:** Different .env files in different directories
**Solution:** Centralize to one .env file, use explicit paths

### **Issue 4: Environment Variables Not Exported**
**Problem:** Variables only available during script execution  
**Solution:** Use shell export for permanent session variables

### **Issue 5: Caching Issues**
**Problem:** Old environment values cached
**Solution:** Restart Python interpreter or use `load_dotenv(override=True)`

---

## 🔒 **Environment Variable Best Practices**

### **1. File Structure**
```
Project/
├── .env                 ← Single source of truth
├── .env.example         ← Template for other developers  
├── LLM/
│   └── accurate_chat.py ← Uses ../env
└── web_app/
    └── app.py           ← Uses ../env
```

### **2. Secure .env Content**
```bash
# .env file
NVIDIA_API_KEY=nvapi-your-actual-key-here
DEBUG=True
PORT=5001
```

### **3. .env.example Template**
```bash
# .env.example file (safe to commit)
NVIDIA_API_KEY=your-nvidia-api-key-here  
DEBUG=False
PORT=5001
```

### **4. Proper Loading Pattern**
```python
import os
from dotenv import load_dotenv

# Method 1: Explicit path (recommended)
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

# Method 2: Search parent directories
load_dotenv(dotenv_path=find_dotenv())

# Method 3: Override existing variables
load_dotenv(override=True)
```

---

## 🚀 **Alternative Solutions**

### **1. Shell Environment (Permanent)**
```bash
# Add to ~/.zshrc or ~/.bash_profile
export NVIDIA_API_KEY="nvapi-your-key-here"
source ~/.zshrc
```

### **2. Conda Environment Variables**
```bash
# Set in conda environment
conda env config vars set NVIDIA_API_KEY=nvapi-your-key-here
conda activate your-env
```

### **3. System Environment (macOS)**
```bash
# Add to system launch agents
launchctl setenv NVIDIA_API_KEY nvapi-your-key-here
```

---

## ✅ **Verification Commands**

```bash
# Check if environment variable is loaded
echo $NVIDIA_API_KEY

# Test Python environment loading
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(f'API Key: {os.getenv(\"NVIDIA_API_KEY\")[:10]}...')"

# Test from specific directory
cd LLM && python -c "import os, sys; sys.path.append('..'); from dotenv import load_dotenv; load_dotenv('../.env'); print('Loaded:', bool(os.getenv('NVIDIA_API_KEY')))"
```

The fixes I applied should resolve your dotenv persistence issues by ensuring the correct path to the .env file is always used, regardless of the working directory when running the scripts.