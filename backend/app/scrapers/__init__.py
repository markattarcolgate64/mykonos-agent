from typing import List, Dict, Any, Optional
import logging
from .base_scraper import ScrapedArticle
from .sources.tech_news_scraper import TechNewsScraper

logger = logging.getLogger(__name__)

class ScraperManager:
    """Manages multiple scrapers and coordinates their execution."""
    
    def __init__(self):
        self.scrapers = {
            'tech_news': TechNewsScraper(),
            # Add more scrapers here as they're implemented
        }
    
    async def scrape_all(self, query: Optional[str] = None) -> List[ScrapedArticle]:
        """Run all configured scrapers and return combined results."""
        all_articles = []
        
        for name, scraper in self.scrapers.items():
            try:
                logger.info(f"Running scraper: {name}")
                articles = await scraper.scrape(query)
                all_articles.extend(articles)
                logger.info(f"Scraper {name} found {len(articles)} articles")
            except Exception as e:
                logger.error(f"Error in scraper {name}: {e}")
                continue
                
        # Sort by publication date, newest first
        all_articles.sort(key=lambda x: x.published_date, reverse=True)
        return all_articles
    
    async def scrape_single(self, source: str, query: Optional[str] = None) -> List[ScrapedArticle]:
        """Run a single scraper by name."""
        if source not in self.scrapers:
            raise ValueError(f"Unknown scraper: {source}")
            
        return await self.scrapers[source].scrape(query)

# Create a default instance for easy importing
scraper_manager = ScraperManager()
