# AI-Powered Micro-Website Generator

> FastAPI backend system that generates unique, AI-powered micro-websites using LLMs and LangChain

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3.0-orange.svg)](https://www.langchain.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-purple.svg)](https://openai.com/)

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Prompt Strategy](#-prompt-strategy)
- [Architecture](#-architecture)
- [Testing](#-testing)
- [Sample Output](#-sample-output)
- [Limitations](#-limitations)
- [Future Improvements](#-future-improvements)

## 🎯 Overview

This system generates thousands of unique micro-websites around a single topic (e.g., "Large Language Models", "Artificial Intelligence") using OpenAI's GPT models orchestrated through LangChain. Each website is truly unique with:

- **Distinct titles and meta descriptions**
- **3-5 varied content sections** with different headings
- **4 different HTML templates** (Modern, Minimal, Classic, Magazine)
- **12+ color schemes** randomly applied
- **Dynamic content generation** with temperature and top-p variations

The system is designed for SEO diversity, audience segmentation, and regional targeting while maintaining topic consistency.

## ✨ Features

### Core Functionality
- ✅ **FastAPI Backend** with automatic OpenAPI documentation
- ✅ **LangChain Integration** for advanced prompt orchestration
- ✅ **OpenAI GPT-3.5-turbo** for content generation
- ✅ **4 Responsive HTML Templates** using Jinja2
- ✅ **Dynamic Prompt Variations** (5+ per prompt type)
- ✅ **Temperature & Top-p Tuning** (0.8-1.0 and 0.85-0.98)
- ✅ **SQLite Logging** for generation history
- ✅ **CLI Tool** for batch generation
- ✅ **Docker Support** with docker-compose
- ✅ **Unit Tests** with pytest

### Diversity Mechanisms
- 🎨 **12 Unique Color Schemes** per website
- 📝 **Random Section Selection** (3-5 from 10 available)
- 🎭 **4 HTML Templates** (Modern, Minimal, Classic, Magazine)
- 🔄 **Dynamic Temperature** variation per generation
- 💬 **8 Prompt Variation Suffixes** for titles
- 🎯 **3 Content Styles** (Educational, Marketing, Technical)

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Docker & Docker Compose (optional, but recommended)

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd micro-website-generator

# Set your OpenAI API key
export OPENAI_API_KEY="sk-your-api-key-here"

# Start the service
docker-compose up --build

# The API will be available at http://localhost:8000
```

### Option 2: Local Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set API key
export OPENAI_API_KEY="sk-your-api-key-here"

# Start server
python app/main.py

# Or use uvicorn directly
uvicorn app.main:app --reload
```

### Verify Installation

Open your browser and navigate to:
- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 📚 API Documentation

### 1. Generate Websites

**Endpoint**: `POST /generate`

Generate multiple unique websites for a given topic.

**Request Body**:
```json
{
  "topic": "Large Language Models",
  "pages_count": 5,
  "style": "educational",
  "max_tokens": 800
}
```

**Parameters**:
- `topic` (string, required): Main topic for website generation
- `pages_count` (integer, default: 5): Number of sites to generate (1-50)
- `style` (string, default: "educational"): Content style - `educational`, `marketing`, or `technical`
- `max_tokens` (integer, default: 800): Maximum tokens per section (100-2000)

**Response**:
```json
{
  "status": "success",
  "topic": "Large Language Models",
  "generated_count": 5,
  "websites": [
    {
      "site_id": "65ada8e8-6bf9-4064-93e7-c1c10781ceca",
      "title": "Revolutionizing Education: The AI Frontier of Learning",
      "meta_description": "Discover the endless possibilities...",
      "file_path": "sites/site_65ada8e8-6bf9-4064-93e7-c1c10781ceca.html",
      "sections_count": 5,
      "tokens_used": 4250,
      "template_style": "modern",
      "timestamp": "2025-10-12T18:44:03.123456"
    }
  ]
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Artificial Intelligence",
    "pages_count": 3,
    "style": "educational",
    "max_tokens": 800
  }'
```

### 2. View Generated Site

**Endpoint**: `GET /site/{site_id}`

Retrieve and display a generated HTML website.

**Example**:
```bash
# Open in browser
http://localhost:8000/site/65ada8e8-6bf9-4064-93e7-c1c10781ceca

# Or use curl
curl http://localhost:8000/site/65ada8e8-6bf9-4064-93e7-c1c10781ceca
```

### 3. View Generation Logs

**Endpoint**: `GET /logs?limit=50`

Get history of all generation requests.

**Response**:
```json
[
  {
    "id": 1,
    "topic": "Artificial Intelligence",
    "pages_count": 5,
    "style": "educational",
    "site_ids": "[\"uuid1\", \"uuid2\", ...]",
    "timestamp": "2025-10-12 18:44:03"
  }
]
```

### 4. View Statistics

**Endpoint**: `GET /stats`

Get aggregated statistics about generations.

**Response**:
```json
{
  "total_generations": 10,
  "total_sites": 47,
  "popular_topics": [
    {"topic": "AI", "count": 5},
    {"topic": "Machine Learning", "count": 3}
  ],
  "style_distribution": [
    {"style": "educational", "count": 6},
    {"style": "marketing", "count": 3},
    {"style": "technical", "count": 1}
  ]
}
```

## 🛠️ CLI Tool

The included CLI utility allows batch generation without the API.

### Basic Usage

```bash
python generate.py --topic "Machine Learning" --count 5
```

### Advanced Usage

```bash
python generate.py \
  --topic "Cloud Computing" \
  --count 10 \
  --style technical \
  --tokens 1000
```

### CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--topic` | Main topic (required) | - |
| `--count` | Number of sites | 5 |
| `--style` | Content style | educational |
| `--tokens` | Max tokens per section | 800 |

### Example Output

```bash
============================================================
Micro-Website Generator CLI
============================================================

Configuration:
  Topic: Machine Learning
  Count: 5
  Style: educational
  Max Tokens: 800

============================================================

Initializing generator...

Generating 5 unique websites...

============================================================
Generation Complete!
============================================================

Time taken: 43.52 seconds
Average: 8.70 seconds per site

Generated 5 websites:

  1. Understanding Machine Learning: A Comprehensive Guide
     ID: abc123...
     File: sites/site_abc123.html
     Sections: 5
     Tokens: ~4100

  ...

============================================================
All websites generated successfully!
============================================================
```

## 🎨 Prompt Strategy

### Diversity Implementation

The system employs multiple layers of diversity to ensure each generated website is unique:

#### 1. **LLM Parameter Variation**
```python
# Random temperature per generation
temperature = random.uniform(0.8, 1.0)

# Random top_p sampling
top_p = random.uniform(0.85, 0.98)
```

#### 2. **Dynamic Prompt Templates**

**Title Generation** (5 variations):
```python
variations = [
    "Create a compelling title about {topic}. Style: {style}. Be unique and engaging.",
    "Generate an innovative title for {topic}. Use {style} tone. Be creative.",
    "Craft a distinctive title covering {topic}. {style} approach. Make it memorable.",
    "Design a captivating title for {topic}. Apply {style} style. Stand out.",
    "Produce an original title focused on {topic}. {style} perspective. Avoid clichés."
]
```

**Plus 8 Variation Suffixes**:
- "Focus on innovation."
- "Emphasize practical aspects."
- "Highlight cutting-edge developments."
- "Stress accessibility and clarity."
- "Showcase real-world impact."
- etc.

#### 3. **Section Diversity**

Each style has 10 different section types, with 3-5 randomly selected:

**Educational Style Sections**:
- Introduction
- Understanding the Fundamentals
- Key Concepts Explained
- Real-World Applications
- Common Challenges and Solutions
- Best Practices
- Future Outlook
- Getting Started
- Resources and Tools
- Conclusion

**Marketing Style Sections**:
- Why This Matters
- Transform Your Business
- Proven Benefits
- Success Stories
- How It Works
- Get Started Today
- Industry Leadership
- What Sets Us Apart
- ROI and Value
- Join Thousands of Satisfied Users

**Technical Style Sections**:
- Technical Overview
- Architecture and Design
- Implementation Details
- API and Integration
- Performance Considerations
- Security Features
- Scalability
- Code Examples
- Troubleshooting
- Advanced Topics

#### 4. **Visual Diversity**

**4 HTML Templates**:
1. **Modern** - Card-based grid layout with gradients
2. **Minimal** - Sidebar navigation with clean design
3. **Classic** - Traditional article layout with serif fonts
4. **Magazine** - Hero section with numbered sections

**12 Color Schemes**:
```python
schemes = [
    {"primary": "#667eea", "secondary": "#764ba2", "accent": "#f093fb"},
    {"primary": "#f093fb", "secondary": "#f5576c", "accent": "#4facfe"},
    {"primary": "#43e97b", "secondary": "#38f9d7", "accent": "#667eea"},
    {"primary": "#fa709a", "secondary": "#fee140", "accent": "#30cfd0"},
    # ... 8 more
]
```

#### 5. **Content Length Variation**

```python
word_count = int(max_tokens * 0.75)  # Converts token limit to approximate words
section_count = random.randint(3, 5)  # Random number of sections
```

### LangChain Integration

The system uses LangChain for:

1. **Prompt Orchestration**: Managing multiple prompt templates
2. **Memory Management**: ConversationBufferMemory for context
3. **LLM Abstraction**: Easy switching between models
4. **Async Support**: Non-blocking content generation

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.9,
    top_p=0.95
)

# Async generation
result = await asyncio.to_thread(llm.invoke, prompt)
```

## 🏗️ Architecture

### System Flow

```
┌─────────────────┐
│  FastAPI Server │
│  (Port 8000)    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  WebsiteGenerator       │
│  - LangChain Manager    │
│  - Prompt Variations    │
│  - Template Selection   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  OpenAI GPT-3.5-turbo   │
│  - Temperature: 0.8-1.0 │
│  - Top-p: 0.85-0.98     │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Jinja2 Templates       │
│  - Modern / Minimal     │
│  - Classic / Magazine   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  HTML Output + SQLite   │
│  sites/site_uuid.html   │
│  generation_logs.db     │
└─────────────────────────┘
```

### Project Structure

```
micro-website-generator/
│
├── app/
│   ├── __init__.py           # Package initialization
│   ├── main.py               # FastAPI entrypoint & routes
│   ├── generator.py          # Core generation logic + LangChain
│   ├── prompts.py            # Prompt templates & variations
│   ├── models.py             # Pydantic models for validation
│   ├── database.py           # SQLite logging
│   └── templates/            # Jinja2 HTML templates
│       ├── site_modern.html
│       ├── site_minimal.html
│       ├── site_classic.html
│       └── site_magazine.html
│
├── sites/                    # Generated HTML files
│   └── site_<uuid>.html
│
├── tests/                    # Unit tests
│   ├── __init__.py
│   └── test_generator.py
│
├── Dockerfile                # Docker container setup
├── docker-compose.yml        # Docker orchestration
├── requirements.txt          # Python dependencies
├── generate.py               # CLI utility
├── generation_logs.db        # SQLite database (created at runtime)
└── README.md                 # This file
```

### Key Components

#### 1. WebsiteGenerator (`app/generator.py`)
- Manages LLM communication via LangChain
- Coordinates prompt generation
- Handles template rendering
- Implements diversity mechanisms

#### 2. PromptManager (`app/prompts.py`)
- Stores all prompt templates
- Manages prompt variations
- Provides section-specific prompts
- Handles style-aware generation

#### 3. Database (`app/database.py`)
- SQLite logging for generations
- Stores metadata for each site
- Provides statistics and history

#### 4. Templates (`app/templates/`)
- Jinja2 HTML templates
- Responsive designs
- Color scheme integration
- SEO-optimized structure

## 🧪 Testing

### Run All Tests

```bash
# Install test dependencies (if not already installed)
pip install pytest pytest-asyncio

# Run all tests with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_generator.py -v
```

### Test Coverage

The test suite covers:

- ✅ Color scheme diversity (20 generations)
- ✅ Prompt variation uniqueness
- ✅ Template generation for all styles
- ✅ Section count randomization (3-5)
- ✅ Content generation mocking
- ✅ Template selection randomness
- ✅ HTML rendering correctness
- ✅ File creation verification

### Example Test Output

```bash
tests/test_generator.py::test_color_scheme_variety PASSED
tests/test_generator.py::test_prompt_variation PASSED
tests/test_generator.py::test_template_styles_exist PASSED
tests/test_generator.py::test_section_count_varies PASSED
tests/test_generator.py::test_content_generation PASSED
tests/test_generator.py::test_random_template_selection PASSED
tests/test_generator.py::test_color_schemes_count PASSED
tests/test_generator.py::test_template_files_created PASSED
tests/test_generator.py::test_html_rendering PASSED

======================== 9 passed in 2.34s =========================
```

## 📊 Sample Output

### Generated Website Examples

The `sites/` folder contains sample generated websites. Here's what to expect:

#### Example 1: Modern Template
- **Topic**: Artificial Intelligence
- **Title**: "Revolutionizing Education: The AI Frontier of Learning"
- **Template**: Modern (card-based grid)
- **Color Scheme**: Teal gradient (#43e97b → #38f9d7)
- **Sections**: 5 (Understanding Fundamentals, Real-World Applications, Getting Started, Key Concepts, Best Practices)

#### Example 2: Minimal Template
- **Topic**: Machine Learning
- **Title**: "Machine Learning Mastery: Your Complete Guide"
- **Template**: Minimal (sidebar navigation)
- **Color Scheme**: Purple gradient (#667eea → #764ba2)
- **Sections**: 4 (Introduction, Applications, Challenges, Future Outlook)

#### Example 3: Classic Template
- **Topic**: Cloud Computing
- **Title**: "Cloud Computing: The Future of Infrastructure"
- **Template**: Classic (traditional article)
- **Color Scheme**: Pink gradient (#fa709a → #fee140)
- **Sections**: 5 (Technical Overview, Architecture, Security, Tools, Summary)

### Quality Characteristics

Each generated website features:

- ✅ **Unique, coherent content** (no templated text)
- ✅ **SEO-optimized meta descriptions** (150-160 characters)
- ✅ **Responsive design** (mobile, tablet, desktop)
- ✅ **Professional styling** with modern CSS
- ✅ **Accessible HTML** with semantic markup
- ✅ **Fast loading** (no external dependencies except fonts)

## ⚠️ Limitations

### Current Constraints

1. **API Dependency**
   - Requires active OpenAI API key
   - Subject to OpenAI rate limits
   - Costs ~$0.002 per website generated

2. **Generation Speed**
   - Average: 5-10 seconds per website
   - Batch generation of 10 sites: ~60-90 seconds
   - Network latency affects performance

3. **Content Quality**
   - English language only (multilingual support possible)
   - Occasional repetition in very similar topics
   - No fact-checking or content validation

4. **Visual Limitations**
   - No image generation (text-only content)
   - Fixed color schemes (no custom theming)
   - 4 template options only

5. **Storage**
   - Local file system only (no cloud storage)
   - No automatic cleanup of old sites
   - SQLite for logging (not production-ready at scale)

### Known Issues

- Extremely long generation times on slow networks
- No retry mechanism for failed API calls
- Limited error handling for malformed prompts

## 🔮 Future Improvements

### High Priority

- [ ] **Image Generation**: Integrate DALL-E 3 for hero images
- [ ] **Caching Layer**: Add Redis for frequently generated topics
- [ ] **Content Similarity Detection**: Prevent duplicate content
- [ ] **Retry Mechanism**: Handle API failures gracefully
- [ ] **Progress Tracking**: WebSocket updates for batch generation

### Medium Priority

- [ ] **More Templates**: Add 5-10 additional design variations
- [ ] **Custom CSS Themes**: User-uploadable color schemes
- [ ] **Multilingual Support**: Generate in multiple languages
- [ ] **SEO Analysis**: Built-in SEO scoring
- [ ] **Export Options**: PDF, DOCX, Markdown export

### Low Priority

- [ ] **A/B Testing**: Compare template performance
- [ ] **Analytics Integration**: Track generated site visits
- [ ] **WordPress Plugin**: Direct publishing to WordPress
- [ ] **Content Scheduling**: Delayed generation jobs
- [ ] **Team Collaboration**: Multi-user support

### Scalability Enhancements

- [ ] **Kubernetes deployment** configuration
- [ ] **PostgreSQL** instead of SQLite
- [ ] **S3/Cloud Storage** for generated files
- [ ] **Celery** for background task processing
- [ ] **Prometheus metrics** for monitoring

## 📝 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-3.5-turbo  # Optional, defaults to gpt-3.5-turbo

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_PATH=generation_logs.db

# Generation Defaults
DEFAULT_STYLE=educational
DEFAULT_MAX_TOKENS=800
```

### Docker Environment

When using Docker, pass environment variables via `docker-compose.yml`:

```yaml
environment:
  - OPENAI_API_KEY=${OPENAI_API_KEY}
  - PYTHONUNBUFFERED=1
```

Or via command line:

```bash
docker run -e OPENAI_API_KEY="sk-..." -p 8000:8000 website-generator
```

## 🤝 Contributing

This is a test task submission, but feedback and suggestions are welcome!

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt
pip install black flake8 mypy

# Format code
black app/ tests/

# Lint
flake8 app/ tests/

# Type checking
mypy app/
```

## 📄 License

This project was created as a technical test task. All rights reserved.

## 🙏 Acknowledgments

- OpenAI for GPT-3.5-turbo API
- LangChain for LLM orchestration framework
- FastAPI for the excellent web framework
- Jinja2 for templating engine

---

**Note**: This project requires an active OpenAI API key. Please ensure you have appropriate usage limits and billing configured before running large batch generations.

For questions or issues, please open an issue on GitHub or contact the author directly.
