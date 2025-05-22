# backend/app/agents/memory.py
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import json

class MemoryItem(BaseModel):
    """A single memory item with content and metadata."""
    content: Any
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Memory:
    """Manages the agent's short-term and long-term memory."""
    
    def __init__(self, max_short_term: int = 100):
        self.short_term: List[MemoryItem] = []
        self.long_term: List[MemoryItem] = []
        self.max_short_term = max_short_term
    
    def add_observation(self, content: Any, metadata: Optional[Dict] = None) -> None:
        """Add a new observation to short-term memory."""
        if metadata is None:
            metadata = {}
            
        item = MemoryItem(content=content, metadata=metadata)
        self.short_term.append(item)
        
        # Move to long-term if short-term is full
        if len(self.short_term) > self.max_short_term:
            self._consolidate_memories()
    
    def retrieve_relevant_memories(self, query: str, limit: int = 5) -> List[MemoryItem]:
        """Retrieve memories relevant to the query (simplified version)."""
        # In a real implementation, you'd use embeddings for semantic search
        all_memories = self.short_term + self.long_term
        return all_memories[:limit]  # Simple implementation
    
    def _consolidate_memories(self) -> None:
        """Move important memories to long-term storage."""
        # Simple implementation: move half of short-term to long-term
        split = len(self.short_term) // 2
        self.long_term.extend(self.short_term[:split])
        self.short_term = self.short_term[split:]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert memories to a dictionary for serialization."""
        return {
            "short_term": [item.dict() for item in self.short_term],
            "long_term": [item.dict() for item in self.long_term]
        }