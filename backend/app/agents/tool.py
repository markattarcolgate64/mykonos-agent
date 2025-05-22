# backend/app/agents/tool.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, Field

class ToolParameter(BaseModel):
    """Definition of a tool parameter."""
    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None

class ToolResult(BaseModel):
    """Result of a tool execution."""
    success: bool
    output: Any
    error: Optional[str] = None

class BaseTool(ABC):
    """Base class for all tools."""
    
    name: str
    description: str
    parameters: Dict[str, ToolParameter] = {}
    
    def __init__(self):
        self._validate()
    
    def _validate(self) -> None:
        """Validate that the tool is properly configured."""
        if not hasattr(self, 'name') or not self.name:
            raise ValueError("Tool must have a name")
        if not hasattr(self, 'description') or not self.description:
            raise ValueError("Tool must have a description")
    
    def get_schema(self) -> Dict[str, Any]:
        """Get the JSON schema for this tool."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    name: {
                        "type": param.type,
                        "description": param.description,
                        "default": param.default
                    }
                    for name, param in self.parameters.items()
                },
                "required": [
                    name for name, param in self.parameters.items()
                    if param.required
                ]
            }
        }
    
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """Execute the tool with the given parameters."""
        pass

class ToolError(Exception):
    """Raised when a tool fails to execute."""
    pass