from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
from dataclasses import dataclass, field
import time
import random
from fake_useragent import UserAgent
import httpx

logger = logging.getLogger(__name__)

@dataclass
class ScrapedArticle:
    """Data class to store scraped article information."""
    title: str
    url: str
    content: str
    published_date: datetime
    source: str
    authors: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    summary: Optional[str] = None
    ai_related: bool = False
    technologies: List[str] = field(default_factory=list)
    job_impact: Dict[str, str] = field(default_factory=dict)

class BaseScraper(ABC):
    """Base class for all scrapers."""
    
    def __init__(self, name: str, base_url: str, rate_limit: float = 1.0):
        self.name = name
        self.base_url = base_url
        self.rate_limit = rate_limit  # seconds between requests
        self.last_request_time = 0
        self.ua = UserAgent()
        
    async def _make_request(self, url: str, method: str = "GET", **kwargs) -> Optional[httpx.Response]:
        """Make an HTTP request with rate limiting and retries."""
        # Enforce rate limiting
        time_since_last = time.time() - self.last_request_time
        if time_since_last < self.rate_limit:
            time.sleep(self.rate_limit - time_since_last)
        
        headers = kwargs.pop('headers', {})
        headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    timeout=30.0,
                    follow_redirects=True,
                    **kwargs
                )
                response.raise_for_status()
                self.last_request_time = time.time()
                return response
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} for {url}: {e}")
        except httpx.RequestError as e:
            logger.error(f"Request failed for {url}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {e}")
            
        return None
    
    @abstractmethod
    async def scrape(self, query: Optional[str] = None) -> List[ScrapedArticle]:
        """
        Main method to perform scraping.
        
        Args:
            query: Optional search query to filter results
            
        Returns:
            List of ScrapedArticle objects
        """
        pass
    
    def _extract_technologies(self, text: str) -> List[str]:
        """Extract technology mentions from text."""
        # This is a simple implementation that can be enhanced with NER or regex patterns
        tech_keywords = [
            'AI', 'ML', 'machine learning', 'deep learning', 'LLM', 'GPT', 'Copilot',
            'GitHub', 'CI/CD', 'Docker', 'Kubernetes', 'automation', 'testing',
            'deployment', 'infrastructure as code', 'Terraform', 'Ansible', 'Jenkins'
        ]
        
        return [tech for tech in tech_keywords if tech.lower() in text.lower()]
    
    def _analyze_job_impact(self, text: str) -> Dict[str, str]:
        """Analyze potential job impact from the article text."""
        # Simple keyword-based analysis - can be enhanced with NLP
        impact_keywords = {
            'junior': ['junior', 'entry-level', 'early career', 'new grad'],
            'mid': ['mid-level', 'experienced', 'senior'],
            'task': ['task automation', 'code generation', 'testing automation'],
            'role': ['role elimination', 'job replacement', 'reduce hiring']
        }
        
        impact = {}
        text_lower = text.lower()
        
        for category, keywords in impact_keywords.items():
            found = [kw for kw in keywords if kw in text_lower]
            if found:
                impact[category] = found
                
        return impact
