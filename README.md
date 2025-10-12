# AI-Powered Micro-Website Generator

FastAPI backend system that generates unique, AI-powered micro-websites using LLMs.

## Features

- FastAPI backend with automatic documentation
- OpenAI GPT integration with diversity tuning
- LangChain for prompt orchestration
- Dynamic content generation with unique titles and descriptions
- Jinja2 HTML templating with randomized color schemes
- SQLite database for generation logs
- CLI tool for batch generation
- Docker support

## Requirements

- Python 3.11+
- OpenAI API key
- Docker (optional)

## Quick Start

### Local Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set API key
export OPENAI_API_KEY="your-api-key-here"

# Start server
python app/main.py