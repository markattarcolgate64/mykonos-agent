#!/usr/bin/env python3
"""
Example usage of the ResearchAgent to find AI news about software engineering automation.
"""
import asyncio
import logging
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.agents.research_agent import ResearchAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    """Run the research agent demo."""
    print("=== AI Research Agent Demo ===\n")
    
    # Initialize the research agent
    agent = ResearchAgent(name="AI Research Assistant")
    
    try:
        # Example 1: Research a specific topic
        print("\n🔍 Researching AI code generation tools...")
        topic_results = await agent.research_topic("AI code generation tools", max_results=3)
        print_results(topic_results)
        
        # Example 2: Get latest developments
        print("\n🚀 Getting latest developments in AI for software engineering...")
        latest_results = await agent.get_latest_developments(days=14)
        print_results(latest_results, show_urls=True)
        
        # Example 3: Compare tools
        print("\n🛠️ Comparing AI coding assistants...")
        comparison = await agent.compare_tools(["GitHub Copilot", "Amazon CodeWhisperer", "Tabnine"])
        print_results(comparison)
        
        # Example 4: Research trends
        print("\n📈 Researching current trends in AI for software engineering...")
        trends = await agent.research_trends()
        print_results(trends)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

def print_results(results: dict, show_urls: bool = False):
    """Print the research results in a readable format."""
    print(f"\n📊 Research Results for: {results.get('topic', 'N/A')}")
    print(f"📅 Date: {results.get('search_date', 'N/A')}")
    print(f"🔢 Results found: {results.get('results_found', 0)}")
    
    # Print analysis summary
    analysis = results.get('analysis', {})
    if analysis:
        print("\n📝 Analysis:")
        print("-" * 50)
        print(analysis.get('summary', 'No analysis available'))
        print("-" * 50)
    
    # Print key points if available
    key_points = analysis.get('key_points', [])
    if key_points:
        print("\n🔑 Key Points:")
        for i, point in enumerate(key_points, 1):
            print(f"{i}. {point}")
    
    # Print result URLs if requested
    if show_urls and results.get('results'):
        print("\n🔗 Sources:")
        for i, result in enumerate(results['results'], 1):
            print(f"{i}. {result.get('title', 'No title')}")
            print(f"   {result.get('url', 'No URL')}")
            if result.get('snippet'):
                print(f"   {result.get('snippet')[:150]}...")
            print()

if __name__ == "__main__":
    asyncio.run(main())
