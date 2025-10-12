"""
SQLite database for logging and persistence
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict
from pathlib import Path


class Database:
    """SQLite database manager for generation logs"""
    
    def __init__(self, db_path: str = "generation_logs.db"):
        self.db_path = db_path
        self.conn = None
    
    def init_db(self):
        """Initialize database and create tables"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS generation_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                pages_count INTEGER NOT NULL,
                style TEXT NOT NULL,
                site_ids TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS site_metadata (
                site_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                meta_description TEXT,
                sections_count INTEGER,
                tokens_used INTEGER,
                file_path TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()
    
    def log_generation(
        self,
        topic: str,
        pages_count: int,
        style: str,
        site_ids: List[str]
    ):
        """Log a generation request"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO generation_logs (topic, pages_count, style, site_ids)
            VALUES (?, ?, ?, ?)
        """, (topic, pages_count, style, json.dumps(site_ids)))
        self.conn.commit()
    
    def save_site_metadata(
        self,
        site_id: str,
        title: str,
        meta_description: str,
        sections_count: int,
        tokens_used: int,
        file_path: str
    ):
        """Save individual site metadata"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO site_metadata 
            (site_id, title, meta_description, sections_count, tokens_used, file_path)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (site_id, title, meta_description, sections_count, tokens_used, file_path))
        self.conn.commit()
    
    def get_logs(self, limit: int = 50) -> List[Dict]:
        """Get generation logs"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, topic, pages_count, style, site_ids, 
                   strftime('%Y-%m-%d %H:%M:%S', timestamp) as timestamp
            FROM generation_logs
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_site_metadata(self, site_id: str) -> Dict:
        """Get metadata for a specific site"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM site_metadata WHERE site_id = ?
        """, (site_id,))
        
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_stats(self) -> Dict:
        """Get generation statistics"""
        cursor = self.conn.cursor()
        
        # Total generations
        cursor.execute("SELECT COUNT(*) as total FROM generation_logs")
        total_generations = cursor.fetchone()['total']
        
        # Total sites
        cursor.execute("SELECT SUM(pages_count) as total FROM generation_logs")
        total_sites = cursor.fetchone()['total'] or 0
        
        # Most popular topics
        cursor.execute("""
            SELECT topic, COUNT(*) as count
            FROM generation_logs
            GROUP BY topic
            ORDER BY count DESC
            LIMIT 5
        """)
        popular_topics = [dict(row) for row in cursor.fetchall()]
        
        # Style distribution
        cursor.execute("""
            SELECT style, COUNT(*) as count
            FROM generation_logs
            GROUP BY style
        """)
        style_distribution = [dict(row) for row in cursor.fetchall()]
        
        return {
            "total_generations": total_generations,
            "total_sites": total_sites,
            "popular_topics": popular_topics,
            "style_distribution": style_distribution
        }
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()