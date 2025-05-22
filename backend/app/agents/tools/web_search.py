from typing import Dict, Any, Optional
from ..tool import BaseTool, ToolResult, ToolParameter
from ...llm.client import llm_client
import logging

logger = logging.getLogger(__name__)

class WebSearchTool(BaseTool):
    """Tool for searching the web for information."""
    
    name = "web_search"
    description = "Search the web for information on a given topic"
    
    parameters = {
        "query": ToolParameter(
            name="query",
            type="string",
            description="The search query",
            required=True
        ),
        "num_results": ToolParameter(
            name="num_results",
            type="integer",
            description="Number of search results to return (default: 5)",
            required=False,
            default=5
        ),
        "domain": ToolParameter(
            name="domain",
            type="string",
            description="Optional domain to recommend the search prioritize",
            required=False
        )
    }
    
    async def execute(self, query: str, num_results: int = 5, domain: Optional[str] = None) -> ToolResult:
        """Execute a web search and return the results."""
        try:
            logger.info(f"Performing web search: {query}")
            
            # Use the search_web tool to get results
            search_results = await llm_client.search_web(
                query=query,
                domain=domain
            )
            
            # Limit the number of results
            if search_results and len(search_results) > num_results:
                search_results = search_results[:num_results]
                
            return ToolResult(
                success=True,
                output={
                    "query": query,
                    "results": search_results or [],
                    "result_count": len(search_results) if search_results else 0
                }
            )
            
        except Exception as e:
            error_msg = f"Error performing web search: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return ToolResult(
                success=False,
                output=None,
                error=error_msg
            )
