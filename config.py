"""
Configuration file for ACTIVA LLM settings.
Supports OpenAI, Claude, and Gemini providers.
"""

import os
import json
from typing import Literal, Optional, cast

# LLM Provider types
ProviderType = Literal["openai", "claude", "gemini"]

# Default configuration
DEFAULT_CONFIG = {
    "provider": "openai",
    "model": "gpt-4o",
    "api_key": "",
    "base_url": None
}

def load_config():
    """
    Load configuration from config.json or environment variables.
    Falls back to defaults if no config is found.
    """
    # Try to load from config.json
    config_file = "config.json"
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
                provider = config_data.get("provider", DEFAULT_CONFIG["provider"])
                # Validate provider type
                if provider not in ["openai", "claude", "gemini"]:
                    provider = DEFAULT_CONFIG["provider"]
                
                return {
                    "provider": cast(ProviderType, provider),
                    "model": config_data.get("model", DEFAULT_CONFIG["model"]),
                    "api_key": config_data.get("api_key", DEFAULT_CONFIG["api_key"]),
                    "base_url": config_data.get("base_url", DEFAULT_CONFIG["base_url"])
                }
        except Exception as e:
            print(f"Warning: Could not load config.json: {e}")
    
    # Fall back to environment variables
    provider = os.getenv("ACTIVA_PROVIDER", DEFAULT_CONFIG["provider"])
    if provider not in ["openai", "claude", "gemini"]:
        provider = DEFAULT_CONFIG["provider"]
    
    model = os.getenv("ACTIVA_MODEL", DEFAULT_CONFIG["model"])
    api_key = os.getenv("ACTIVA_API_KEY", DEFAULT_CONFIG["api_key"])
    base_url = os.getenv("ACTIVA_BASE_URL", DEFAULT_CONFIG["base_url"])
    
    return {
        "provider": cast(ProviderType, provider),
        "model": model,
        "api_key": api_key,
        "base_url": base_url
    }

def create_config_file():
    """Create a sample config.json file with default settings."""
    sample_config = {
        "provider": "openai",
        "model": "gpt-4o",
        "api_key": "your-api-key-here",
        "base_url": None,
        "_comment": "Supported providers: openai, claude, gemini"
    }
    
    with open("config.json", 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    print("✅ Created config.json with sample configuration")
    print("📝 Please edit config.json with your API key and preferred settings")

def get_llm_client(config):
    """
    Get the appropriate LLM client based on the configuration.
    Returns a client that can be used with LangGraph.
    """
    try:
        if config["provider"] == "openai":
            from langchain_openai import ChatOpenAI
            kwargs = {
                "model": config["model"],
                "openai_api_key": config["api_key"],
            }
            if config["base_url"]:
                kwargs["openai_api_base"] = config["base_url"]
            return ChatOpenAI(**kwargs)
        
        elif config["provider"] == "claude":
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model=config["model"],
                anthropic_api_key=config["api_key"]
            )
        
        elif config["provider"] == "gemini":
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(
                model=config["model"],
                google_api_key=config["api_key"]
            )
        
        else:
            raise ValueError(f"Unsupported provider: {config['provider']}")
    except ImportError as e:
        print(f"Error: Missing dependency for {config['provider']}. Please install required packages.")
        print(f"Install with: pip install langchain-{config['provider']}")
        raise

# Load configuration on import
config = load_config() 