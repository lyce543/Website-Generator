"""
FastAPI Backend for Micro-Website Generator
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from app.models import GenerateRequest, GenerateResponse, LogEntry
from app.generator import WebsiteGenerator
from app.database import Database

db = Database()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager"""
    db.init_db()
    Path("sites").mkdir(exist_ok=True)
    
    # Print startup message with localhost URL
    print("\n" + "=" * 60)
    print("🚀 Micro-Website Generator API")
    print("=" * 60)
    print(f"📍 API:  http://localhost:8000")
    print(f"📚 Docs: http://localhost:8000/docs")
    print("=" * 60 + "\n")
    
    yield
    db.close()

app = FastAPI(
    title="Micro-Website Generator API",
    description="Generate unique AI-powered micro-websites",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

generator = WebsiteGenerator()


@app.get("/", response_class=HTMLResponse)
async def root():
    """Simple web interface for demo"""
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Micro-Website Generator</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        }
        h1 { color: #667eea; margin-bottom: 1rem; }
        h3 { color: #333; margin-top: 2rem; margin-bottom: 1rem; }
        .form-group { margin-bottom: 1rem; }
        label { display: block; margin-bottom: 0.5rem; font-weight: 500; color: #333; }
        input, select { 
            width: 100%; 
            padding: 0.5rem; 
            border: 1px solid #ddd; 
            border-radius: 4px;
            font-size: 1rem;
        }
        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            background: #667eea;
            color: white;
            padding: 0.75rem 2rem;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 1rem;
            width: 100%;
            margin-top: 1rem;
        }
        button:hover { background: #5568d3; }
        button:disabled { 
            background: #ccc; 
            cursor: not-allowed; 
        }
        #result { 
            margin-top: 2rem; 
            padding: 1rem; 
            background: #f8f9fa; 
            border-radius: 4px;
            display: none;
        }
        #result.show { display: block; }
        .site-link { 
            color: #667eea; 
            text-decoration: none; 
            font-weight: 500;
        }
        .site-link:hover { text-decoration: underline; }
        .site-card {
            margin-bottom: 1rem; 
            padding: 1rem; 
            background: white; 
            border-radius: 4px;
            border: 1px solid #e0e0e0;
        }
        .site-card strong {
            color: #333;
            font-size: 1.1rem;
        }
        .site-card small {
            color: #666;
            display: block;
            margin: 0.5rem 0;
        }
        hr { 
            margin: 2rem 0; 
            border: none; 
            border-top: 1px solid #ddd; 
        }
        .api-links {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        .api-links a {
            padding: 0.5rem;
            border-radius: 4px;
            transition: background 0.2s;
        }
        .api-links a:hover {
            background: #f8f9fa;
        }
        .subtitle {
            color: #666;
            margin-bottom: 2rem;
        }
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 10px;
            vertical-align: middle;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Micro-Website Generator</h1>
        <p class="subtitle">Generate unique AI-powered websites using LLMs</p>
        
        <form id="generateForm">
            <div class="form-group">
                <label>Topic:</label>
                <input type="text" id="topic" value="Artificial Intelligence" required>
            </div>
            
            <div class="form-group">
                <label>Number of sites:</label>
                <input type="number" id="count" value="3" min="1" max="10" required>
            </div>
            
            <div class="form-group">
                <label>Style:</label>
                <select id="style">
                    <option value="educational">Educational</option>
                    <option value="marketing">Marketing</option>
                    <option value="technical">Technical</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Max tokens per section:</label>
                <input type="number" id="tokens" value="800" min="100" max="2000" required>
            </div>
            
            <button type="submit" id="submitBtn">Generate Websites</button>
        </form>
        
        <div id="result"></div>
        
        <hr>
        
        <h3>API Documentation</h3>
        <div class="api-links">
            <a href="/docs" class="site-link">→ Swagger UI Documentation</a>
            <a href="/logs" class="site-link">→ View Generation Logs (JSON)</a>
            <a href="/stats" class="site-link">→ View Statistics (JSON)</a>
        </div>
    </div>
    
    <script>
        const form = document.getElementById('generateForm');
        const resultDiv = document.getElementById('result');
        const submitBtn = document.getElementById('submitBtn');
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="loading"></span>Generating...';
            resultDiv.className = 'show';
            resultDiv.innerHTML = '<p>⏳ Generating websites... This may take 10-30 seconds.</p>';
            
            const data = {
                topic: document.getElementById('topic').value,
                pages_count: parseInt(document.getElementById('count').value),
                style: document.getElementById('style').value,
                max_tokens: parseInt(document.getElementById('tokens').value)
            };
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const result = await response.json();
                
                let html = '<h3>✅ Generated Successfully!</h3>';
                html += `<p>Topic: <strong>${result.topic}</strong></p>`;
                html += `<p>Generated: <strong>${result.generated_count}</strong> websites</p><br>`;
                
                result.websites.forEach((site, i) => {
                    html += `<div class="site-card">`;
                    html += `<strong>${i + 1}. ${site.title}</strong><br>`;
                    html += `<small>${site.meta_description}</small>`;
                    html += `<a href="/site/${site.site_id}" target="_blank" class="site-link">→ Open Website</a>`;
                    html += `</div>`;
                });
                
                resultDiv.innerHTML = html;
            } catch (error) {
                resultDiv.innerHTML = `<p style="color: red;">❌ Error: ${error.message}</p>`;
            } finally {
                // Reset button state
                submitBtn.disabled = false;
                submitBtn.textContent = 'Generate Websites';
            }
        });
    </script>
</body>
</html>
"""


@app.post("/generate", response_model=GenerateResponse)
async def generate_websites(request: GenerateRequest):
    """
    Generate multiple unique websites for a given topic
    """
    try:
        websites = await generator.generate_multiple(
            topic=request.topic,
            count=request.pages_count,
            style=request.style,
            max_tokens=request.max_tokens
        )
        
        db.log_generation(
            topic=request.topic,
            pages_count=request.pages_count,
            style=request.style,
            site_ids=[site["site_id"] for site in websites]
        )
        
        return GenerateResponse(
            status="success",
            topic=request.topic,
            generated_count=len(websites),
            websites=websites
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@app.get("/site/{site_id}")
async def get_site(site_id: str):
    """
    Retrieve generated HTML site by ID
    """
    site_path = Path(f"sites/site_{site_id}.html")
    
    if not site_path.exists():
        raise HTTPException(status_code=404, detail="Site not found")
    
    return FileResponse(site_path, media_type="text/html")


@app.get("/logs", response_model=list[LogEntry])
async def get_logs(limit: int = 50):
    """
    Get generation history logs
    """
    logs = db.get_logs(limit=limit)
    return logs


@app.get("/stats")
async def get_stats():
    """
    Get generation statistics
    """
    stats = db.get_stats()
    return stats


if __name__ == "__main__":
    print("=" * 60)
    print("Starting Micro-Website Generator API")
    print("=" * 60)
    print("API: http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    print("=" * 60)
    
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0", 
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\nServer stopped")