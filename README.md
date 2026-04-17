# LangChainLanguageNvidia

NVIDIA RAG LLM project with LangChain integration for building AI-powered applications using NVIDIA's AI endpoints.

## Features

- 🚀 LangChain integration with NVIDIA AI endpoints
- 🔒 Secure API key management using environment variables
- 🤖 RAG (Retrieval-Augmented Generation) capabilities
- 📦 Easy setup with virtual environment

## Prerequisites

- Python 3.8 or higher
- NVIDIA API key (get one from [NVIDIA AI](https://build.nvidia.com/))

## Installation

1. Clone the repository:
```bash
git clone https://github.com/whbBBHR/LangChainLanguageNvidia.git
cd LangChainLanguageNvidia
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

> **Note for Anaconda/Conda users**: If you have an existing conda environment with older LangChain packages (e.g., `langchain-core` 0.3.x), run the following to ensure compatible versions are installed:
> ```bash
> pip install --upgrade -r requirements.txt
> ```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your NVIDIA API key
```

## Usage

Run the main script:
```bash
python nvidia_rag_llm.py
```

## Project Structure

```
.
├── nvidia_rag_llm.py      # Main script with NVIDIA AI integration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variable template
├── .gitignore           # Git ignore rules for Python projects
└── README.md            # This file
```

## Environment Variables

- `NVIDIA_API_KEY`: Your NVIDIA AI API key (required)

## Dependencies

- `langchain-core>=1.2.5`: Core LangChain primitives (required for `ModelProfile` support)
- `langchain>=1.0.0`: LangChain framework for building AI applications
- `langchain-nvidia-ai-endpoints>=1.0.0`: NVIDIA AI endpoints integration
- `python-dotenv>=1.0.0`: Environment variable management

## License

This project is open source and available under the MIT License.