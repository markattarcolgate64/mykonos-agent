import logging
from typing import Dict, Any, List, Optional, Union
import json
import time
from functools import lru_cache

from openai import OpenAI, AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from ..config.llm_config import llm_config

logger = logging.getLogger(__name__)


class LLMClient:
    """Client for interacting with various LLM providers."""
    
    def __init__(self, config=None):
        """Initialize the LLM client with configuration."""
        self.config = config or llm_config
        self._setup_clients()
    
    def _setup_clients(self):
        """Set up clients for different providers."""
        self.openai_client = None
        self.async_openai_client = None
        
        if self.config.provider == "openai" and self.config.openai_api_key:
            self.openai_client = OpenAI(
                api_key=self.config.openai_api_key,
                organization=self.config.openai_organization
            )
            self.async_openai_client = AsyncOpenAI(
                api_key=self.config.openai_api_key,
                organization=self.config.openai_organization
            )
        elif self.config.provider == "anthropic":
            # Add Anthropic client setup when needed
            pass
    
    @lru_cache(maxsize=128)
    def _get_cached_response(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get a cached response if available and not expired."""
        # In a production environment, you might want to use Redis or similar
        # For now, we'll just use in-memory caching with lru_cache
        return None
    
    def _create_cache_key(self, prompt: str, **kwargs) -> str:
        """Create a cache key for the given prompt and parameters."""
        params = {
            "prompt": prompt,
            **{k: v for k, v in kwargs.items() if k not in ['stream', 'timeout']}
        }
        return json.dumps(params, sort_keys=True)
    
    async def generate_async(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> Dict[str, Any]:
        """Generate a response asynchronously."""
        if self.config.provider == "openai" and self.async_openai_client:
            return await self._generate_openai_async(messages, **kwargs)
        else:
            raise NotImplementedError(f"Async generation not implemented for provider: {self.config.provider}")
    
    async def _generate_openai_async(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> Dict[str, Any]:
        """Generate a response using OpenAI's async API."""
        if not self.async_openai_client:
            raise ValueError("OpenAI client not properly initialized")
        
        # Merge default parameters with overrides
        params = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            **kwargs
        }
        
        try:
            response = await self.async_openai_client.chat.completions.create(**params)
            return {
                "content": response.choices[0].message.content,
                "usage": response.usage.dict() if hasattr(response, 'usage') and response.usage else None,
                "model": response.model,
                "finish_reason": response.choices[0].finish_reason
            }
        except Exception as e:
            logger.error(f"Error in OpenAI API call: {str(e)}")
            raise
    
    def generate(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> Dict[str, Any]:
        """Generate a response synchronously."""
        if self.config.provider == "openai" and self.openai_client:
            return self._generate_openai(messages, **kwargs)
        else:
            raise NotImplementedError(f"Synchronous generation not implemented for provider: {self.config.provider}")
    
    def _generate_openai(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> Dict[str, Any]:
        """Generate a response using OpenAI's sync API."""
        if not self.openai_client:
            raise ValueError("OpenAI client not properly initialized")
        
        # Merge default parameters with overrides
        params = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            **kwargs
        }
        
        try:
            response = self.openai_client.chat.completions.create(**params)
            return {
                "content": response.choices[0].message.content,
                "usage": response.usage.dict() if hasattr(response, 'usage') and response.usage else None,
                "model": response.model,
                "finish_reason": response.choices[0].finish_reason
            }
        except Exception as e:
            logger.error(f"Error in OpenAI API call: {str(e)}")
            raise

# Create a singleton instance
llm_client = LLMClient()
