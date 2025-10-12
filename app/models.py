"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class GenerateRequest(BaseModel):
    """Request model for website generation"""
    topic: str = Field(..., description="Main topic for website generation")
    pages_count: int = Field(default=5, ge=1, le=50, description="Number of sites to generate")
    style: str = Field(default="educational", description="Content style: educational, marketing, or technical")
    max_tokens: int = Field(default=800, ge=100, le=2000, description="Maximum tokens per section")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "topic": "Large Language Models",
                "pages_count": 5,
                "style": "educational",
                "max_tokens": 800
            }
        }
    }


class WebsiteMetadata(BaseModel):
    """Metadata for a generated website"""
    site_id: str
    title: str
    meta_description: str
    file_path: str
    sections_count: int
    tokens_used: int
    timestamp: str


class GenerateResponse(BaseModel):
    """Response model for generation endpoint"""
    status: str
    topic: str
    generated_count: int
    websites: List[WebsiteMetadata]


class LogEntry(BaseModel):
    """Log entry for generation history"""
    id: int
    topic: str
    pages_count: int
    style: str
    site_ids: str
    timestamp: str


class SectionContent(BaseModel):
    """Model for individual content section"""
    heading: str
    content: str
    section_type: Optional[str] = None