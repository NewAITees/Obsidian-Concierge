"""
Configuration management utilities.

This module provides functionality for loading and managing application configuration
from YAML files and environment variables.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    """Application configuration model."""
    
    # Server settings
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    
    # Logging settings
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FILE: Optional[str] = Field(default=None, description="Log file path")
    
    # Database settings
    CHROMA_DB_DIR: str = Field(
        default="./data/chroma",
        description="ChromaDB persistence directory"
    )
    
    # LLM settings
    OLLAMA_HOST: str = Field(
        default="http://localhost:11434",
        description="Ollama API host"
    )
    OLLAMA_MODEL: str = Field(
        default="gemma:7b",
        description="Ollama model name"
    )
    
    # Security settings
    SECRET_KEY: str = Field(
        default="your-secret-key",
        description="Secret key for JWT"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Access token expiration time in minutes"
    )


def load_config(config_path: Optional[str] = None) -> AppConfig:
    """
    Load application configuration from YAML file and environment variables.
    
    Args:
        config_path: Path to the YAML configuration file
        
    Returns:
        AppConfig instance with loaded configuration
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid
    """
    # Default configuration
    config_dict: Dict[str, Any] = {}
    
    # Load from config file if provided
    if config_path:
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
            
        with open(config_file, "r") as f:
            try:
                config_dict = yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise yaml.YAMLError(f"Invalid YAML in config file: {e}")
    
    # Override with environment variables
    for field in AppConfig.__fields__:
        env_value = os.getenv(field)
        if env_value is not None:
            config_dict[field] = env_value
    
    return AppConfig(**config_dict)


# Default configuration instance
config = load_config() 