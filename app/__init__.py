"""
Micro-Website Generator
AI-powered system for generating unique micro-websites
"""

__version__ = "1.0.0"
__author__ = "AI Backend Developer"

from app.generator import WebsiteGenerator
from app.models import GenerateRequest, GenerateResponse, WebsiteMetadata
from app.database import Database

__all__ = [
    "WebsiteGenerator",
    "GenerateRequest",
    "GenerateResponse",
    "WebsiteMetadata",
    "Database",
]