# AI Automation Tracker - Scraper Module

This module provides a flexible and extensible framework for scraping and analyzing content related to AI automation in software engineering.

## Features

- **Modular Architecture**: Easily add new scrapers for different sources
- **Asynchronous Processing**: Fast and efficient scraping with `httpx`
- **Rate Limiting**: Built-in rate limiting to avoid overwhelming target sites
- **Content Analysis**: Automatic extraction of technologies and job impact
- **REST API**: FastAPI-based endpoints for integration with other services

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the API**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`

3. **Test the Scraper**
   ```bash
   python scripts/test_scraper.py
   ```
   This will run the scrapers and save results to a JSON file.

## API Endpoints

- `GET /` - API information and available endpoints
- `GET /scrape` - Scrape all sources
  - Query params: `?query=search+term` (optional)
- `GET /sources` - List available scraping sources
- `GET /scrape/{source}` - Scrape a specific source

## Adding a New Scraper

1. Create a new file in `backend/app/scrapers/sources/`
2. Create a class that inherits from `BaseScraper`
3. Implement the `scrape()` method
4. Add an instance to `scraper_manager` in `backend/app/scrapers/__init__.py`

Example:

```python
from ..base_scraper import BaseScraper, ScrapedArticle

class MyScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="my_source",
            base_url="https://example.com",
            rate_limit=2.0
        )
    
    async def scrape(self, query=None):
        # Your scraping logic here
        return []
```

## Configuration

Environment variables can be set in a `.env` file:

```
# Database URL (SQLite by default)
DATABASE_URL=sqlite:///./automation.db

# Request timeout (seconds)
REQUEST_TIMEOUT=30.0
```

## Testing

Run the test script:

```bash
python scripts/test_scraper.py
```

## License

MIT
