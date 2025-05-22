from typing import Dict, Any, List, Optional
from .simple_agent import AIAgent, AgentState, Observation
from .tool import ToolResult, BaseTool
from .tools.web_search import WebSearchTool
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ResearchAgent(AIAgent):
    """
    A specialized agent for researching AI news related to software engineering automation.
    """
    
    def __init__(self, name: str = "AI Research Agent"):
        """Initialize the research agent with necessary tools."""
        role = """
        You are an AI research assistant specialized in finding and analyzing the latest news 
        about AI in software engineering automation. Your goal is to provide comprehensive, 
        accurate, and up-to-date information about AI tools, frameworks, and methodologies 
        that are transforming software engineering practices.
        """
        
        # Initialize the base AI agent
        super().__init__(
            name=name,
            role=role,
            tools=[WebSearchTool()]  # Add web search capability
        )
        
        # Additional configuration specific to research
        self.search_domains = [
            "github.com",
            "techcrunch.com",
            "venturebeat.com",
            "towardsdatascience.com",
            "medium.com",
            "reddit.com/r/MachineLearning",
            "news.ycombinator.com"
        ]
        
        logger.info(f"Initialized Research Agent: {self.name}")
    
    async def research_topic(self, topic: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Research a specific topic related to AI in software engineering automation.
        
        Args:
            topic: The specific aspect of AI in software engineering to research
            max_results: Maximum number of search results to return
            
        Returns:
            Dict containing research results and analysis
        """
        self.state = AgentState.THINKING
        
        try:
            # Log the research request
            logger.info(f"Starting research on topic: {topic}")
            
            # Create a more focused search query
            search_query = f"{topic} AI software engineering automation"
            
            # Search across preferred domains
            all_results = []
            
            for domain in self.search_domains:
                search_result = await self.act(
                    "web_search",
                    {"query": f"site:{domain} {search_query}", "num_results": 3}
                )
                
                if search_result.success and search_result.output.get("results"):
                    all_results.extend(search_result.output["results"])
            
            # If no domain-specific results, do a general search
            if not all_results:
                search_result = await self.act(
                    "web_search",
                    {"query": search_query, "num_results": max_results * 2}
                )
                if search_result.success and search_result.output.get("results"):
                    all_results = search_result.output["results"]
            
            # Limit results and remove duplicates
            unique_results = []
            seen_urls = set()
            
            for result in all_results:
                if result.get("url") and result["url"] not in seen_urls:
                    unique_results.append(result)
                    seen_urls.add(result["url"])
                    if len(unique_results) >= max_results:
                        break
            
            # Analyze the results
            analysis = await self._analyze_results(unique_results, topic)
            
            # Create the final research result
            research_result = {
                "topic": topic,
                "search_date": datetime.utcnow().isoformat(),
                "sources_searched": len(self.search_domains) + 1,  # +1 for general search
                "results_found": len(unique_results),
                "results": unique_results,
                "analysis": analysis
            }
            
            # Save to memory
            await self.observe(
                "research",
                f"Completed research on {topic}",
                {"topic": topic, "results_summary": analysis.get("summary", "")}
            )
            
            return research_result
            
        except Exception as e:
            logger.error(f"Error during research on {topic}: {str(e)}", exc_info=True)
            self.state = AgentState.ERROR
            raise
        finally:
            if self.state != AgentState.ERROR:
                self.state = AgentState.IDLE
    
    async def _analyze_results(self, results: List[Dict[str, Any]], topic: str) -> Dict[str, Any]:
        """Analyze search results and extract key insights."""
        if not results:
            return {"summary": "No relevant information found.", "key_points": []}
        
        # Prepare results for analysis
        results_text = "\n\n".join([
            f"Source: {r.get('title', 'No title')} ({r.get('url', 'No URL')})\n"
            f"Snippet: {r.get('snippet', 'No snippet available')}"
            for r in results
        ])
        
        # Use LLM to analyze the results
        system_prompt = """You are an expert AI research analyst. Your task is to analyze search results 
        about AI in software engineering automation and extract key insights, trends, and important information.
        Be concise but thorough in your analysis."""
        
        user_prompt = f"""Please analyze the following search results about '{topic}' in the context of 
        AI in software engineering automation. Provide:
        
        1. A 2-3 paragraph summary of the current state of this topic
        2. 3-5 key points or trends
        3. Any notable tools, frameworks, or companies mentioned
        4. Potential implications for software engineering
        
        Search Results:
        {results_text}"""
        
        try:
            analysis = await self._llm_generate(
                prompt=user_prompt,
                system_message=system_prompt,
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract key points from the analysis
            key_points = []
            if "key points" in analysis.lower() or "1." in analysis:
                # Simple extraction of key points if they're numbered
                import re
                points = re.findall(r'(?:\d+\.\s*|•\s*)([^\n]+)', analysis)
                if points:
                    key_points = [p.strip() for p in points if p.strip()]
            
            return {
                "summary": analysis,
                "key_points": key_points or ["No specific key points extracted."],
                "analysis_date": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing results: {str(e)}", exc_info=True)
            return {
                "summary": "Error analyzing search results.",
                "key_points": ["Analysis failed due to an error."],
                "error": str(e)
            }
    
    async def get_latest_developments(self, days: int = 7) -> Dict[str, Any]:
        """
        Get the latest developments in AI for software engineering automation.
        
        Args:
            days: Number of days to look back for developments
            
        Returns:
            Dict containing latest developments and analysis
        """
        query = f"latest developments in AI for software engineering automation last {days} days"
        return await self.research_topic(query)
    
    async def compare_tools(self, tool_names: List[str]) -> Dict[str, Any]:
        """
        Compare different AI tools for software engineering automation.
        
        Args:
            tool_names: List of tool names to compare
            
        Returns:
            Dict containing comparison analysis
        """
        if not tool_names:
            return {"error": "No tools provided for comparison"}
            
        query = f"compare {' vs '.join(tool_names)} for software engineering automation"
        return await self.research_topic(query)
    
    async def research_trends(self) -> Dict[str, Any]:
        """
        Research current trends in AI for software engineering automation.
        
        Returns:
            Dict containing trend analysis
        """
        return await self.research_topic("emerging trends in AI for software engineering automation")
