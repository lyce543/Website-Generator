"""
Website generation logic with enhanced diversity and LangChain integration
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
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from app.prompts import PromptManager


class WebsiteGenerator:
    """Generate unique micro-websites using LLMs with enhanced diversity"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.9,
            top_p=0.95,
            api_key=self.api_key
        )
        
        self.prompt_manager = PromptManager()
        self.memory = ConversationBufferMemory()
        
        template_dir = Path(__file__).parent / "templates"
        template_dir.mkdir(exist_ok=True)
        self.jinja_env = Environment(loader=FileSystemLoader(str(template_dir)))
        
        self._ensure_templates()
    
    def _ensure_templates(self):
        templates = {
            "modern": self._get_modern_template(),
            "minimal": self._get_minimal_template(),
            "classic": self._get_classic_template(),
            "magazine": self._get_magazine_template()
        }
        
        for name, content in templates.items():
            template_path = Path(__file__).parent / "templates" / f"site_{name}.html"
            if not template_path.exists():
                template_path.parent.mkdir(exist_ok=True)
                with open(template_path, 'w', encoding='utf-8') as f:
                    f.write(content)
    
    def _get_modern_template(self) -> str:
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
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, {{ color_scheme.primary }} 0%, {{ color_scheme.secondary }} 100%);
            min-height: 100vh;
            padding: 2rem;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        header {
            background: white;
            padding: 3rem;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
            margin-bottom: 2rem;
            text-align: center;
        }
        h1 { 
            font-size: 3rem; 
            background: linear-gradient(135deg, {{ color_scheme.primary }}, {{ color_scheme.accent }});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 1rem;
        }
        .meta { color: #666; font-size: 1.1rem; }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }
        .card {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        .card:hover { transform: translateY(-10px); }
        .card h2 {
            color: {{ color_scheme.primary }};
            margin-bottom: 1rem;
            font-size: 1.8rem;
        }
        .card p { line-height: 1.8; color: #444; }
        footer {
            text-align: center;
            margin-top: 3rem;
            color: white;
            padding: 2rem;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{{ title }}</h1>
            <p class="meta">{{ meta_description }}</p>
        </header>
        
        <div class="grid">
            {% for section in sections %}
            <div class="card">
                <h2>{{ section.heading }}</h2>
                <p>{{ section.content }}</p>
            </div>
            {% endfor %}
        </div>
        
        <footer>
            <p>Generated: {{ timestamp }} | ID: {{ site_id }}</p>
        </footer>
    </div>
</body>
</html>"""
    
    def _get_minimal_template(self) -> str:
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
            font-family: 'Arial', sans-serif;
            display: flex;
            min-height: 100vh;
            background: #f5f5f5;
        }
        aside {
            width: 280px;
            background: {{ color_scheme.primary }};
            color: white;
            padding: 2rem;
            position: fixed;
            height: 100vh;
            overflow-y: auto;
        }
        aside h1 { font-size: 1.8rem; margin-bottom: 2rem; }
        aside nav a {
            display: block;
            color: white;
            text-decoration: none;
            padding: 0.8rem;
            margin: 0.5rem 0;
            border-radius: 5px;
            transition: background 0.2s;
        }
        aside nav a:hover { background: rgba(255,255,255,0.2); }
        main {
            margin-left: 280px;
            padding: 3rem;
            flex: 1;
        }
        section {
            background: white;
            padding: 2.5rem;
            margin-bottom: 2rem;
            border-left: 5px solid {{ color_scheme.accent }};
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        h2 { 
            color: {{ color_scheme.primary }}; 
            margin-bottom: 1.5rem;
            font-size: 2rem;
        }
        p { line-height: 1.9; color: #333; }
        @media (max-width: 768px) {
            aside { position: relative; width: 100%; height: auto; }
            main { margin-left: 0; }
        }
    </style>
</head>
<body>
    <aside>
        <h1>{{ title }}</h1>
        <p style="opacity: 0.9; margin-bottom: 2rem;">{{ meta_description }}</p>
        <nav>
            {% for section in sections %}
            <a href="#section-{{ loop.index }}">{{ section.heading }}</a>
            {% endfor %}
        </nav>
    </aside>
    
    <main>
        {% for section in sections %}
        <section id="section-{{ loop.index }}">
            <h2>{{ section.heading }}</h2>
            <p>{{ section.content }}</p>
        </section>
        {% endfor %}
        
        <footer style="text-align: center; padding: 2rem; color: #666;">
            Generated: {{ timestamp }} | ID: {{ site_id }}
        </footer>
    </main>
</body>
</html>"""
    
    def _get_classic_template(self) -> str:
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
            font-family: Georgia, 'Times New Roman', serif;
            background: #fafafa;
            line-height: 1.8;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 40px rgba(0,0,0,0.1);
        }
        header {
            border-top: 8px solid {{ color_scheme.primary }};
            border-bottom: 3px double {{ color_scheme.primary }};
            padding: 3rem 2rem;
            text-align: center;
            background: {{ color_scheme.secondary }};
            color: white;
        }
        h1 {
            font-size: 2.8rem;
            font-weight: 700;
            letter-spacing: -1px;
            margin-bottom: 1rem;
        }
        .meta {
            font-style: italic;
            font-size: 1.1rem;
            opacity: 0.95;
        }
        article {
            padding: 3rem 4rem;
        }
        section {
            break-inside: avoid;
            margin-bottom: 3rem;
        }
        h2 {
            font-size: 1.9rem;
            color: {{ color_scheme.primary }};
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid {{ color_scheme.accent }};
        }
        p { 
            text-align: justify;
            margin-bottom: 1.2rem;
            color: #222;
        }
        footer {
            border-top: 3px double {{ color_scheme.primary }};
            padding: 2rem;
            text-align: center;
            background: #f9f9f9;
            font-size: 0.9rem;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{{ title }}</h1>
            <p class="meta">{{ meta_description }}</p>
        </header>
        
        <article>
            {% for section in sections %}
            <section>
                <h2>{{ section.heading }}</h2>
                <p>{{ section.content }}</p>
            </section>
            {% endfor %}
        </article>
        
        <footer>
            <p>Published: {{ timestamp }}</p>
            <p>Document ID: {{ site_id }}</p>
        </footer>
    </div>
</body>
</html>"""
    
    def _get_magazine_template(self) -> str:
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
            font-family: 'Helvetica Neue', Arial, sans-serif;
            background: white;
        }
        .hero {
            height: 70vh;
            background: linear-gradient(135deg, {{ color_scheme.primary }}, {{ color_scheme.secondary }});
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: white;
            padding: 2rem;
            position: relative;
            overflow: hidden;
        }
        .hero::before {
            content: '';
            position: absolute;
            width: 150%;
            height: 150%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
            background-size: 50px 50px;
            animation: moveGrid 20s linear infinite;
        }
        @keyframes moveGrid {
            0% { transform: translate(0, 0); }
            100% { transform: translate(50px, 50px); }
        }
        .hero-content {
            position: relative;
            z-index: 1;
            max-width: 800px;
        }
        h1 {
            font-size: 4rem;
            font-weight: 900;
            margin-bottom: 1.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .meta {
            font-size: 1.3rem;
            line-height: 1.6;
            opacity: 0.95;
        }
        .content {
            max-width: 1100px;
            margin: 0 auto;
            padding: 4rem 2rem;
        }
        section {
            margin-bottom: 4rem;
            display: flex;
            gap: 3rem;
            align-items: flex-start;
        }
        section:nth-child(even) { flex-direction: row-reverse; }
        .section-number {
            font-size: 5rem;
            font-weight: 900;
            color: {{ color_scheme.accent }};
            opacity: 0.3;
            min-width: 100px;
        }
        .section-content { flex: 1; }
        h2 {
            font-size: 2.2rem;
            color: {{ color_scheme.primary }};
            margin-bottom: 1.5rem;
        }
        p {
            line-height: 1.9;
            color: #333;
            font-size: 1.05rem;
        }
        footer {
            background: #111;
            color: white;
            text-align: center;
            padding: 3rem 2rem;
        }
        @media (max-width: 768px) {
            h1 { font-size: 2.5rem; }
            section { flex-direction: column !important; }
            .section-number { font-size: 3rem; }
        }
    </style>
</head>
<body>
    <div class="hero">
        <div class="hero-content">
            <h1>{{ title }}</h1>
            <p class="meta">{{ meta_description }}</p>
        </div>
    </div>
    
    <div class="content">
        {% for section in sections %}
        <section>
            <div class="section-number">{{ loop.index }}</div>
            <div class="section-content">
                <h2>{{ section.heading }}</h2>
                <p>{{ section.content }}</p>
            </div>
        </section>
        {% endfor %}
    </div>
    
    <footer>
        <p style="margin-bottom: 0.5rem;">AI Generated Content</p>
        <p>{{ timestamp }} | {{ site_id }}</p>
    </footer>
</body>
</html>"""
    
    async def generate_multiple(
        self,
        topic: str,
        count: int,
        style: str = "educational",
        max_tokens: int = 800
    ) -> List[Dict]:
        websites = []
        template_styles = ["modern", "minimal", "classic", "magazine"]
        
        for i in range(count):
            temp_variation = random.uniform(0.8, 1.0)
            top_p_variation = random.uniform(0.85, 0.98)
            
            template_style = random.choice(template_styles)
            
            self.llm.temperature = temp_variation
            self.llm.top_p = top_p_variation
            
            website = await self._generate_single(
                topic=topic,
                style=style,
                max_tokens=max_tokens,
                index=i,
                template_style=template_style
            )
            websites.append(website)
        
        return websites
    
    async def _generate_single(
        self,
        topic: str,
        style: str,
        max_tokens: int,
        index: int,
        template_style: str
    ) -> Dict:
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
            color_scheme=color_scheme,
            template_name=template_style
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
            "template_style": template_style,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _generate_content(self, prompt: str) -> str:
        try:
            result = await asyncio.to_thread(self.llm.invoke, prompt)
            return result.content.strip() if hasattr(result, 'content') else str(result).strip()
        except Exception as e:
            print(f"Error generating content: {e}")
            return "Generated content"
    
    async def _generate_sections(self, section_prompts: List[Dict]) -> List[Dict]:
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
        color_scheme: Dict,
        template_name: str = "modern"
    ) -> str:
        template = self.jinja_env.get_template(f"site_{template_name}.html")
        
        return template.render(
            site_id=site_id,
            title=title,
            meta_description=meta_description,
            sections=sections,
            color_scheme=color_scheme,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    
    def _get_random_colors(self) -> Dict:
        schemes = [
            {"primary": "#667eea", "secondary": "#764ba2", "accent": "#f093fb"},
            {"primary": "#f093fb", "secondary": "#f5576c", "accent": "#4facfe"},
            {"primary": "#43e97b", "secondary": "#38f9d7", "accent": "#667eea"},
            {"primary": "#fa709a", "secondary": "#fee140", "accent": "#30cfd0"},
            {"primary": "#a8edea", "secondary": "#fed6e3", "accent": "#667eea"},
            {"primary": "#ff9a9e", "secondary": "#fecfef", "accent": "#667eea"},
            {"primary": "#ffecd2", "secondary": "#fcb69f", "accent": "#ff6e7f"},
            {"primary": "#e0c3fc", "secondary": "#8ec5fc", "accent": "#667eea"},
            {"primary": "#09203f", "secondary": "#537895", "accent": "#ffd700"},
            {"primary": "#ee0979", "secondary": "#ff6a00", "accent": "#00f2fe"},
            {"primary": "#0f2027", "secondary": "#203a43", "accent": "#2c5364"},
            {"primary": "#360033", "secondary": "#0b8793", "accent": "#ff512f"},
        ]
        return random.choice(schemes)