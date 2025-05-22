from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum
from typing import Optional, Literal

class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"

class LLMConfig(BaseSettings):
    """Configuration for LLM integration."""
    
    # Provider settings
    provider: LLMProvider = LLMProvider.OPENAI
    model: str = "gpt-4-turbo-preview"
    temperature: float = 0.7
    max_tokens: int = 2000
    
    # OpenAI specific settings
    openai_api_key: Optional[str] = None
    openai_organization: Optional[str] = None
    
    # Anthropic specific settings
    anthropic_api_key: Optional[str] = None
    
    # Local model settings
    local_model_path: Optional[str] = None
    local_model_device: Literal["cpu", "cuda", "mps"] = "cpu"
    
    # Rate limiting and retries
    max_retries: int = 3
    request_timeout: int = 30  # seconds
    
    # Caching
    enable_caching: bool = True
    cache_ttl: int = 3600  # 1 hour in seconds
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="LLM_",
        extra="ignore"
    )

# Create a singleton instance
llm_config = LLMConfig()

def update_llm_config(**kwargs) -> None:
    """Update the LLM configuration."""
    global llm_config
    llm_config = LLMConfig(**{**llm_config.model_dump(), **kwargs})
