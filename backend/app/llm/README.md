# LLM Integration

This module provides integration with various Large Language Models (LLMs) for the agent system.

## Features

- Support for multiple LLM providers (OpenAI, Anthropic, local models)
- Synchronous and asynchronous API
- Caching for improved performance
- Configuration via environment variables
- Easy integration with the agent system

## Configuration

1. Copy `.env.example` to `.env` in the backend directory:
   ```bash
   cp .env.example .env
   ```

2. Update the `.env` file with your API keys and configuration.

## Usage

### Basic Usage

```python
from app.llm.client import llm_client

# Synchronous generation
response = llm_client.generate([
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, how are you?"}
])
print(response["content"])

# Asynchronous generation
async def get_response():
    response = await llm_client.generate_async([
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ])
    return response["content"]
```

### Using with Agents

The `AIAgent` class has been updated to use the LLM client by default. You can use the helper methods:

```python
# Generate text with a system message
text = await agent._llm_generate(
    prompt="Tell me a joke",
    system_message="You are a helpful assistant that tells funny jokes.",
    temperature=0.8
)

# Have a conversation
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What's the weather like?"}
]
response = await agent._llm_chat(messages)
```

## Available Methods

### LLMClient

- `generate(messages, **kwargs)`: Generate a response synchronously
- `generate_async(messages, **kwargs)`: Generate a response asynchronously

### AIAgent

- `_llm_generate(prompt, system_message=None, **kwargs)`: Generate text with an optional system message
- `_llm_chat(messages, **kwargs)`: Have a conversation with the LLM

## Configuration Options

See `.env.example` for all available configuration options. The most important ones are:

- `LLM_PROVIDER`: The LLM provider to use (openai, anthropic, local)
- `LLM_MODEL`: The model to use (e.g., gpt-4-turbo-preview)
- `LLM_TEMPERATURE`: Controls randomness (0.0 to 1.0)
- `LLM_MAX_TOKENS`: Maximum number of tokens to generate

## Adding a New Provider

1. Add the provider to the `LLMProvider` enum in `config/llm_config.py`
2. Update the `_setup_clients` method in `llm/client.py` to initialize the new client
3. Add provider-specific configuration options to `LLMConfig`
4. Implement the generation methods for the new provider
