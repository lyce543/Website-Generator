#!/usr/bin/env python3
"""
CLI utility for generating websites
Usage: python generate.py --topic "AI" --count 5 --style educational
"""
import asyncio
import argparse
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from app.generator import WebsiteGenerator
from app.database import Database


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Generate AI-powered micro-websites",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate.py --topic "Machine Learning" --count 5
  python generate.py --topic "Cloud Computing" --count 10 --style technical
        """
    )
    
    parser.add_argument("--topic", type=str, required=True, help="Main topic")
    parser.add_argument("--count", type=int, default=5, help="Number of sites (default: 5)")
    parser.add_argument("--style", type=str, choices=["educational", "marketing", "technical"], 
                       default="educational", help="Content style (default: educational)")
    parser.add_argument("--tokens", type=int, default=800, help="Max tokens per section (default: 800)")
    
    return parser.parse_args()


async def main():
    """Main CLI function"""
    args = parse_args()
    
    print("=" * 60)
    print("Micro-Website Generator CLI")
    print("=" * 60)
    print(f"\nConfiguration:")
    print(f"  Topic: {args.topic}")
    print(f"  Count: {args.count}")
    print(f"  Style: {args.style}")
    print(f"  Max Tokens: {args.tokens}")
    print("\n" + "=" * 60)
    
    Path("sites").mkdir(exist_ok=True)
    
    db = Database()
    db.init_db()
    
    try:
        print("\nInitializing generator...")
        generator = WebsiteGenerator()
        
        print(f"\nGenerating {args.count} unique websites...")
        start_time = datetime.now()
        
        websites = await generator.generate_multiple(
            topic=args.topic,
            count=args.count,
            style=args.style,
            max_tokens=args.tokens
        )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        site_ids = [site["site_id"] for site in websites]
        db.log_generation(
            topic=args.topic,
            pages_count=args.count,
            style=args.style,
            site_ids=site_ids
        )
        
        print("\n" + "=" * 60)
        print("Generation Complete!")
        print("=" * 60)
        print(f"\nTime taken: {duration:.2f} seconds")
        print(f"Average: {duration/args.count:.2f} seconds per site")
        print(f"\nGenerated {len(websites)} websites:\n")
        
        for i, site in enumerate(websites, 1):
            print(f"  {i}. {site['title']}")
            print(f"     ID: {site['site_id']}")
            print(f"     File: {site['file_path']}")
            print(f"     Sections: {site['sections_count']}")
            print(f"     Tokens: ~{site['tokens_used']}")
            print()
        
        print("=" * 60)
        print("All websites generated successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        sys.exit(1)
    
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())