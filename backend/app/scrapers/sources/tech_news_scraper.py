from typing import List, Optional
from datetime import datetime
import logging
from bs4 import BeautifulSoup
import feedparser
from newspaper import Article

from ..base_scraper import BaseScraper, ScrapedArticle

logger = logging.getLogger(__name__)

class TechNewsScraper(BaseScraper):
    """Scraper for general technology news sites with RSS feeds."""
    
    def __init__(self):
        super().__init__(
            name="tech_news",
            base_url="https://news.google.com/rss",
            rate_limit=2.0
        )
        # List of tech news RSS feeds to monitor
        self.feeds = [
            "https://techcrunch.com/feed/",
            "https://www.theverge.com/rss/index.xml",
            "https://feeds.feedburner.com/TechCrunch/",
            "https://www.wired.com/feed/rss"
        ]
    
    async def scrape(self, query: Optional[str] = None) -> List[ScrapedArticle]:
        """Scrape articles from configured tech news RSS feeds."""
        articles = []
        
        for feed_url in self.feeds:
            try:
                # Parse the RSS feed
                feed = feedparser.parse(feed_url)
                print("feed", feed)
                for entry in feed.entries[:10]:
                    try:
                        article = await self._process_entry(entry)
                        if article:
                            articles.append(article)
                    except Exception as e:
                        logger.error(f"Error processing entry {entry.get('link')}: {e}")
                        continue
                        
            except Exception as e:
                logger.error(f"Error processing feed {feed_url}: {e}")
                continue
                
        return articles
    
    async def _process_entry(self, entry) -> Optional[ScrapedArticle]:
        """Process a single RSS entry into a ScrapedArticle."""
        url = entry.get('link')
        if not url:
            return None
            
        # Skip if not related to AI/automation
        title = entry.get('title', '').lower()
        summary = entry.get('summary', '').lower()
        if not any(term in f"{title} {summary}" for term in ['ai', 'artificial intelligence', 'automation', 'ml', 'machine learning']):
            return None
            
        # Download and parse the full article
        try:
            article = Article(url)
            article.download()
            article.parse()
            
            # Extract authors
            authors = article.authors or [author.get('name', '') for author in entry.get('authors', [])]
            
            # Parse published date
            published = entry.get('published_parsed')
            published_date = datetime(*published[:6]) if published else datetime.utcnow()
            
            # Create ScrapedArticle
            return ScrapedArticle(
                title=article.title or entry.get('title', 'No title'),
                url=url,
                content=article.text,
                published_date=published_date,
                source=entry.get('source', {}).get('title', self.name),
                authors=authors,
                keywords=article.keywords or [],
                summary=article.summary or entry.get('summary', ''),
                ai_related=True,
                technologies=self._extract_technologies(article.text),
                job_impact=self._analyze_job_impact(article.text)
            )
            
        except Exception as e:
            logger.error(f"Error processing article {url}: {e}")
            return None
