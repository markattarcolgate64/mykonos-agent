from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import logging

from .scrapers import scraper_manager, ScrapedArticle
from .scrapers.base_scraper import ScrapedArticle as ScrapedArticleModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Automation Tracker API",
              description="API for tracking AI automation in software engineering")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "AI Automation Tracker API",
        "endpoints": {
            "scrape": "/scrape",
            "sources": "/sources",
            "scrape_source": "/scrape/{source}",
        }
    }

@app.get("/scrape", response_model=List[ScrapedArticleModel])
async def scrape_all(query: Optional[str] = Query(None, description="Optional search query")):
    """
    Scrape all configured sources for AI automation content.
    """
    try:
        articles = await scraper_manager.scrape_all(query)
        return articles
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sources")
async def list_sources():
    """List all available scraping sources."""
    return {"sources": list(scraper_manager.scrapers.keys())}

@app.get("/scrape/{source}", response_model=List[ScrapedArticleModel])
async def scrape_source(
    source: str,
    query: Optional[str] = Query(None, description="Optional search query")
):
    """
    Scrape a specific source for AI automation content.
    """
    try:
        articles = await scraper_manager.scrape_single(source, query)
        return articles
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error during scraping {source}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
