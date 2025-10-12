"""
Website generation logic with LLM integration
"""
import os
import random
import uuid
import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from jinja2 import Environment, FileSystemLoader

from langchain_openai import ChatOpenAI
from app.prompts import PromptManager


class WebsiteGenerator:
    """Generate unique micro-websites using LLMs"""
    
    def __init__(self, api_key: str = None):
        """Initialize generator with LLM client"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        # Fixed: specify top_p explicitly instead of in model_kwargs
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.9,
            top_p=0.95,  # Moved from model_kwargs
            api_key=self.api_key
        )
        
        self.prompt_manager = PromptManager()
        
        template_dir = Path(__file__).parent / "templates"
        template_dir.mkdir(exist_ok=True)
        self.jinja_env = Environment(loader=FileSystemLoader(str(template_dir)))
        
        self._ensure_template()
    
    def _ensure_template(self):
        """Ensure HTML template exists"""
        template_path = Path(__file__).parent / "templates" / "site_template.html"
        if not template_path.exists():
            template_path.parent.mkdir(exist_ok=True)
            with open(template_path, 'w') as f:
                f.write(self._get_template())
    
    def _get_template(self) -> str:
        """Get HTML template"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{{ meta_description }}">
    <meta name="keywords" content="{{ title }}, technology, innovation">
    <meta name="author" content="AI Website Generator">
    <title>{{ title }}</title>
    <style>
        * { 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
        }
        
        :root {
            --primary: {{ color_scheme.primary }};
            --secondary: {{ color_scheme.secondary }};
            --accent: {{ color_scheme.accent }};
            --text: #2d3748;
            --text-light: #4a5568;
            --bg-light: #f7fafc;
            --border: #e2e8f0;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
            line-height: 1.7;
            color: var(--text);
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            min-height: 100vh;
            padding: 2rem 1rem;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            overflow: hidden;
        }
        
        /* Header */
        header {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><rect width="100" height="100" fill="none"/><circle cx="50" cy="50" r="40" fill="white" opacity="0.05"/></svg>');
            opacity: 0.1;
        }
        
        h1 {
            font-size: 2.75rem;
            font-weight: 800;
            margin-bottom: 1rem;
            line-height: 1.2;
            position: relative;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .meta {
            font-size: 1.125rem;
            opacity: 0.95;
            max-width: 800px;
            margin: 0 auto;
            line-height: 1.6;
            position: relative;
        }
        
        /* Navigation */
        nav {
            background: white;
            border-bottom: 1px solid var(--border);
            padding: 1rem 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        nav ul {
            list-style: none;
            display: flex;
            gap: 2rem;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        nav a {
            color: var(--text);
            text-decoration: none;
            font-weight: 500;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            transition: all 0.2s;
        }
        
        nav a:hover {
            background: var(--bg-light);
            color: var(--primary);
        }
        
        /* Main Content */
        main {
            padding: 3rem 2rem;
        }
        
        section {
            margin-bottom: 4rem;
            animation: fadeIn 0.6s ease-in-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        section:hover {
            transform: translateX(0);
        }
        
        h2 {
            font-size: 2rem;
            color: var(--primary);
            margin-bottom: 1.5rem;
            padding-bottom: 0.75rem;
            border-bottom: 3px solid var(--accent);
            display: inline-block;
        }
        
        h2::before {
            content: '▸ ';
            color: var(--accent);
            font-weight: bold;
        }
        
        .content {
            background: var(--bg-light);
            padding: 2rem;
            border-radius: 12px;
            border-left: 4px solid var(--accent);
            position: relative;
            overflow: hidden;
        }
        
        .content::before {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 100px;
            height: 100px;
            background: var(--accent);
            opacity: 0.05;
            border-radius: 50%;
            transform: translate(30%, -30%);
        }
        
        p {
            margin-bottom: 1.25rem;
            text-align: justify;
            line-height: 1.8;
            color: var(--text-light);
            position: relative;
        }
        
        p:first-letter {
            font-size: 1.5em;
            font-weight: bold;
            color: var(--primary);
        }
        
        /* Highlight boxes */
        .highlight {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1.5rem 0;
            border-left: 4px solid var(--primary);
        }
        
        /* Footer */
        footer {
            background: linear-gradient(to right, var(--bg-light), white);
            padding: 2rem;
            text-align: center;
            border-top: 1px solid var(--border);
        }
        
        .footer-content {
            max-width: 800px;
            margin: 0 auto;
        }
        
        .site-info {
            display: flex;
            justify-content: center;
            gap: 2rem;
            flex-wrap: wrap;
            margin-top: 1rem;
            font-size: 0.9rem;
            color: var(--text-light);
        }
        
        .site-id {
            font-family: 'Courier New', monospace;
            background: var(--bg-light);
            padding: 0.5rem 1rem;
            border-radius: 6px;
            border: 1px solid var(--border);
            font-size: 0.85rem;
        }
        
        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            background: var(--accent);
            color: white;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            body {
                padding: 1rem 0.5rem;
            }
            
            h1 {
                font-size: 2rem;
            }
            
            header {
                padding: 2rem 1rem;
            }
            
            main {
                padding: 2rem 1rem;
            }
            
            nav ul {
                gap: 1rem;
            }
            
            nav a {
                padding: 0.4rem 0.8rem;
                font-size: 0.9rem;
            }
        }
        
        /* Print styles */
        @media print {
            body {
                background: white;
            }
            
            .container {
                box-shadow: none;
            }
            
            nav {
                display: none;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{{ title }}</h1>
            <p class="meta">{{ meta_description }}</p>
        </header>
        
        <nav>
            <ul>
                {% for section in sections %}
                <li><a href="#section-{{ loop.index }}">{{ section.heading }}</a></li>
                {% endfor %}
            </ul>
        </nav>
        
        <main>
            {% for section in sections %}
            <section id="section-{{ loop.index }}">
                <h2>{{ section.heading }}</h2>
                <div class="content">
                    <p>{{ section.content }}</p>
                </div>
            </section>
            {% endfor %}
            
            <div class="highlight">
                <p><strong>💡 Key Takeaway:</strong> This content was generated using advanced AI technology to provide unique, informative content tailored to your needs.</p>
            </div>
        </main>
        
        <footer>
            <div class="footer-content">
                <span class="badge">AI Generated</span>
                <div class="site-info">
                    <span>📅 Generated: {{ timestamp }}</span>
                    <span>🆔 ID: <span class="site-id">{{ site_id }}</span></span>
                </div>
            </div>
        </footer>
    </div>
</body>
</html>"""
    
    async def generate_multiple(
        self,
        topic: str,
        count: int,
        style: str = "educational",
        max_tokens: int = 800
    ) -> List[Dict]:
        """Generate multiple unique websites"""
        websites = []
        
        for i in range(count):
            # Vary temperature and top_p for each generation
            temp_variation = random.uniform(0.8, 1.0)
            top_p_variation = random.uniform(0.9, 0.95)
            
            # Update LLM parameters
            self.llm.temperature = temp_variation
            self.llm.top_p = top_p_variation  # Updated: direct assignment
            
            website = await self._generate_single(
                topic=topic,
                style=style,
                max_tokens=max_tokens,
                index=i
            )
            websites.append(website)
        
        return websites
    
    async def _generate_single(
        self,
        topic: str,
        style: str,
        max_tokens: int,
        index: int
    ) -> Dict:
        """Generate a single website"""
        site_id = str(uuid.uuid4())
        
        title_prompt = self.prompt_manager.get_title_prompt(topic, style, index)
        meta_prompt = self.prompt_manager.get_meta_prompt(topic, style)
        section_prompts = self.prompt_manager.get_section_prompts(topic, style, max_tokens)
        
        title = await self._generate_content(title_prompt)
        meta_description = await self._generate_content(meta_prompt)
        sections = await self._generate_sections(section_prompts)
        
        color_scheme = self._get_random_colors()
        
        html_content = self._render_html(
            site_id=site_id,
            title=title,
            meta_description=meta_description,
            sections=sections,
            color_scheme=color_scheme
        )
        
        file_path = f"sites/site_{site_id}.html"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        tokens_used = len(html_content.split()) * 1.3
        
        return {
            "site_id": site_id,
            "title": title,
            "meta_description": meta_description,
            "file_path": file_path,
            "sections_count": len(sections),
            "tokens_used": int(tokens_used),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _generate_content(self, prompt: str) -> str:
        """Generate content using LLM"""
        try:
            result = await asyncio.to_thread(self.llm.invoke, prompt)
            return result.content.strip() if hasattr(result, 'content') else str(result).strip()
        except Exception as e:
            print(f"Error generating content: {e}")
            return "Generated content"
    
    async def _generate_sections(self, section_prompts: List[Dict]) -> List[Dict]:
        """Generate content sections"""
        sections = []
        
        for section_data in section_prompts:
            try:
                result = await asyncio.to_thread(
                    self.llm.invoke,
                    section_data["prompt"]
                )
                
                content = result.content if hasattr(result, 'content') else str(result)
                
                sections.append({
                    "heading": section_data["heading"],
                    "content": content.strip()
                })
            except Exception as e:
                print(f"Error generating section {section_data['heading']}: {e}")
                sections.append({
                    "heading": section_data["heading"],
                    "content": "Content generation in progress..."
                })
        
        return sections
    
    def _render_html(
        self,
        site_id: str,
        title: str,
        meta_description: str,
        sections: List[Dict],
        color_scheme: Dict
    ) -> str:
        """Render HTML using Jinja2"""
        template = self.jinja_env.get_template("site_template.html")
        
        return template.render(
            site_id=site_id,
            title=title,
            meta_description=meta_description,
            sections=sections,
            color_scheme=color_scheme,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    
    def _get_random_colors(self) -> Dict:
        """Get random color scheme"""
        schemes = [
            {"primary": "#667eea", "secondary": "#764ba2", "accent": "#f093fb"},
            {"primary": "#f093fb", "secondary": "#f5576c", "accent": "#4facfe"},
            {"primary": "#43e97b", "secondary": "#38f9d7", "accent": "#667eea"},
            {"primary": "#fa709a", "secondary": "#fee140", "accent": "#30cfd0"},
            {"primary": "#a8edea", "secondary": "#fed6e3", "accent": "#667eea"},
            {"primary": "#ff9a9e", "secondary": "#fecfef", "accent": "#667eea"},
            {"primary": "#ffecd2", "secondary": "#fcb69f", "accent": "#ff6e7f"},
            {"primary": "#e0c3fc", "secondary": "#8ec5fc", "accent": "#667eea"},
        ]
        return random.choice(schemes)