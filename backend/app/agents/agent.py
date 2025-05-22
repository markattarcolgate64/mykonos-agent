# backend/app/agents/simple_agent.py
from typing import Dict, Any, List, Optional, Callable, Awaitable
from pydantic import BaseModel, Field
from datetime import datetime
import logging
from enum import Enum

from ..llm.client import llm_client
from .memory import Memory
from .tool import BaseTool, ToolResult

# Type aliases
LLMResponse = Dict[str, Any]
LLMHandler = Callable[..., Awaitable[LLMResponse]]

logger = logging.getLogger(__name__)

class AgentState(str, Enum):
    """Represents the possible states of an agent."""
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    ERROR = "error"

class Observation(BaseModel):
    """Represents an observation made by the agent."""
    source: str
    content: Any
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AIAgent:
    """Base class for AI agents with tools and memory.
    
    This class provides the core functionality for agents that can use tools,
    maintain memory, and interact with LLMs.
    """
    
    def __init__(
        self,
        name: str,
        role: str,
        tools: Optional[List[BaseTool]] = None,
        memory: Optional[Memory] = None
    ) -> None:
        """Initialize the AI agent.
        
        Args:
            name: The name of the agent
            role: The role or purpose of the agent
            tools: List of tools the agent can use
            memory: Memory instance for storing observations (creates new if None)
        """
        self.name = name
        self.role = role
        self.state = AgentState.IDLE
        self.memory = memory or Memory()
        
        # Initialize tools
        self.tools: Dict[str, BaseTool] = {}
        if tools:
            for tool in tools:
                self.add_tool(tool)
    
    def add_tool(self, tool: BaseTool) -> None:
        """Register a tool with the agent."""
        if tool.name in self.tools:
            raise ValueError(f"Tool with name '{tool.name}' already exists")
        self.tools[tool.name] = tool
    
    def get_tool(self, tool_name: str) -> BaseTool:
        """Get a tool by name."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")
        return self.tools[tool_name]
    
    async def observe(self, source: str, content: Any, metadata: Optional[Dict] = None) -> None:
        """Record an observation."""
        self.memory.add_observation(content, metadata or {})
        logger.info(f"[{self.name}] Observed from {source}: {str(content)[:100]}...")
    
    async def _llm_generate(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        **kwargs
    ) -> str:
        """Generate text using the LLM with the given prompt and system message."""
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = await llm_client.generate_async(messages, **kwargs)
            return response["content"]
        except Exception as e:
            logger.error(f"Error in LLM generation: {str(e)}")
            raise
    
    async def act(self, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an action using one of the agent's tools."""
        self.state = AgentState.ACTING
        
        try:
            tool = self.get_tool(action)
            result = await tool.execute(**parameters)
            
            # Log the action and result
            await self.observe(
                "action_result",
                f"Executed {action}",
                {"action": action, "parameters": parameters, "result": result.dict()}
            )
            
            return {
                "success": result.success,
                "output": result.output,
                "error": result.error
            }
            
        except Exception as e:
            error_msg = f"Error executing action {action}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {"success": False, "output": None, "error": error_msg}
        finally:
            self.state = AgentState.IDLE
