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
    <title>{{ title }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, {{ color_scheme.primary }} 0%, {{ color_scheme.secondary }} 100%);
            min-height: 100vh;
            padding: 2rem;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 3rem;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        }
        h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            color: {{ color_scheme.accent }};
            border-bottom: 4px solid {{ color_scheme.accent }};
            padding-bottom: 0.5rem;
        }
        .meta {
            color: #666;
            font-size: 0.95rem;
            margin-bottom: 2rem;
            padding: 1rem;
            background: #f8f9fa;
            border-left: 4px solid {{ color_scheme.accent }};
        }
        section {
            margin: 2.5rem 0;
            padding: 1.5rem;
            background: #fafafa;
            border-radius: 8px;
            transition: transform 0.2s;
        }
        section:hover {
            transform: translateX(10px);
            box-shadow: -5px 0 15px rgba(0,0,0,0.1);
        }
        h2 {
            font-size: 1.8rem;
            margin-bottom: 1rem;
            color: {{ color_scheme.secondary }};
        }
        p {
            margin-bottom: 1rem;
            text-align: justify;
        }
        .footer {
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 2px solid #eee;
            text-align: center;
            color: #999;
            font-size: 0.9rem;
        }
        .site-id {
            font-family: 'Courier New', monospace;
            background: #f0f0f0;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ title }}</h1>
        <div class="meta">
            {{ meta_description }}
        </div>
        
        {% for section in sections %}
        <section>
            <h2>{{ section.heading }}</h2>
            <p>{{ section.content }}</p>
        </section>
        {% endfor %}
        
        <div class="footer">
            <p>Generated on {{ timestamp }}</p>
            <p>Site ID: <span class="site-id">{{ site_id }}</span></p>
        </div>
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