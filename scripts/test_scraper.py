#!/usr/bin/env python3
"""
Test script for the web scraper.
"""
import asyncio
import json
from datetime import datetime
from pathlib import Path

# Add the project root to the Python path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from backend.app.scrapers import scraper_manager

def save_results(articles, filename=None):
    """Save scraping results to a JSON file."""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scraping_results_{timestamp}.json"
    
    # Convert datetime objects to ISO format for JSON serialization
    def json_serial(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump([article.__dict__ for article in articles], f, default=json_serial, indent=2)
    
    print(f"Saved {len(articles)} articles to {filename}")

async def main():
    """Run the scraper and display results."""
    print("Starting scraper test...")
    
    # List available sources
    sources = list(scraper_manager.scrapers.keys())
    print(f"Available sources: {', '.join(sources)}")
    
    # Scrape all sources
    print("\nScraping all sources...")
    articles = await scraper_manager.scrape_all(query="AI automation software engineering")
    print(f"Found {len(articles)} articles total")
    
    # Save results
    save_results(articles)
    
    # Show a sample article
    if articles:
        print("\nSample article:")
        sample = articles[0]
        print(f"Title: {sample.title}")
        print(f"Source: {sample.source}")
        print(f"Published: {sample.published_date}")
        print(f"URL: {sample.url}")
        print(f"Technologies: {', '.join(sample.technologies)}")
        print(f"Job Impact: {sample.job_impact}")
        print(f"Summary: {sample.summary[:200]}...")

if __name__ == "__main__":
    asyncio.run(main())
