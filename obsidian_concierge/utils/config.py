"""
Configuration management module.

This module provides functionality for loading and managing application configuration
from various sources (YAML files, environment variables).
"""

import os
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    """Application configuration model."""
    
    # Server settings
    HOST: str = Field(default="127.0.0.1", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    
    # Logging settings
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FILE: str = Field(default="app.log", description="Log file path")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log message format"
    )
    LOG_MAX_BYTES: int = Field(
        default=10_485_760,  # 10MB
        description="Maximum size of log file before rotation"
    )
    LOG_BACKUP_COUNT: int = Field(
        default=5,
        description="Number of backup log files to keep"
    )
    
    # ChromaDB settings
    CHROMA_DB_DIR: str = Field(
        default="data/chromadb",
        description="Directory for ChromaDB persistence"
    )
    CHROMA_COLLECTION_NAME: str = Field(
        default="obsidian_notes",
        description="Name of the ChromaDB collection"
    )
    
    # Vault settings
    VAULT_PATH: str = Field(
        default="vault",
        description="Path to Obsidian vault"
    )
    VAULT_INDEX_BATCH_SIZE: int = Field(
        default=100,
        description="Number of documents to process in each indexing batch"
    )


def load_config(config_path: Optional[str] = None) -> AppConfig:
    """
    Load application configuration.
    
    Args:
        config_path: Path to YAML configuration file
        
    Returns:
        Application configuration
    """
    config_data = {}
    
    # Load from YAML file if provided
    if config_path:
        config_path = Path(config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
            
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f) or {}
    
    # Override with environment variables
    for field in AppConfig.__fields__:
        env_value = os.getenv(field)
        if env_value is not None:
            config_data[field] = env_value
    
    return AppConfig(**config_data)


# Global configuration instance
config = load_config() 