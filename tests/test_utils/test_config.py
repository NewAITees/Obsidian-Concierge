"""
Tests for configuration management module.
"""

import os
import pytest
import yaml
from pathlib import Path

from obsidian_concierge.utils.config import AppConfig, load_config


@pytest.fixture
def config_file(tmp_path):
    """Fixture for temporary config file."""
    config_data = {
        "HOST": "localhost",
        "PORT": 9000,
        "LOG_LEVEL": "DEBUG",
        "LOG_FILE": "test.log",
        "LOG_FORMAT": "%(levelname)s - %(message)s",
        "LOG_MAX_BYTES": 5_242_880,  # 5MB
        "LOG_BACKUP_COUNT": 3,
        "CHROMA_DB_DIR": "test/chromadb",
        "CHROMA_COLLECTION_NAME": "test_collection",
        "VAULT_PATH": "test/vault",
        "VAULT_INDEX_BATCH_SIZE": 50
    }
    
    config_file = tmp_path / "config.yaml"
    with open(config_file, "w") as f:
        yaml.dump(config_data, f)
    
    return config_file


def test_default_config():
    """Test loading default configuration."""
    config = AppConfig()
    
    # Server settings
    assert config.HOST == "127.0.0.1"
    assert config.PORT == 8000
    
    # Logging settings
    assert config.LOG_LEVEL == "INFO"
    assert config.LOG_FILE == "app.log"
    assert "%(asctime)s" in config.LOG_FORMAT
    assert config.LOG_MAX_BYTES == 10_485_760
    assert config.LOG_BACKUP_COUNT == 5
    
    # ChromaDB settings
    assert config.CHROMA_DB_DIR == "data/chromadb"
    assert config.CHROMA_COLLECTION_NAME == "obsidian_notes"
    
    # Vault settings
    assert config.VAULT_PATH == "vault"
    assert config.VAULT_INDEX_BATCH_SIZE == 100


def test_config_from_yaml(config_file):
    """Test loading configuration from YAML file."""
    config = load_config(str(config_file))
    
    assert config.HOST == "localhost"
    assert config.PORT == 9000
    assert config.LOG_LEVEL == "DEBUG"
    assert config.LOG_FILE == "test.log"
    assert config.LOG_FORMAT == "%(levelname)s - %(message)s"
    assert config.LOG_MAX_BYTES == 5_242_880
    assert config.LOG_BACKUP_COUNT == 3
    assert config.CHROMA_DB_DIR == "test/chromadb"
    assert config.CHROMA_COLLECTION_NAME == "test_collection"
    assert config.VAULT_PATH == "test/vault"
    assert config.VAULT_INDEX_BATCH_SIZE == 50


def test_config_from_env():
    """Test loading configuration from environment variables."""
    env_vars = {
        "HOST": "0.0.0.0",
        "PORT": "7000",
        "LOG_LEVEL": "WARNING",
        "CHROMA_DB_DIR": "env/chromadb",
        "VAULT_PATH": "env/vault",
        "VAULT_INDEX_BATCH_SIZE": "200"
    }
    
    # Set environment variables
    for key, value in env_vars.items():
        os.environ[key] = value
    
    try:
        config = load_config()
        
        assert config.HOST == "0.0.0.0"
        assert config.PORT == 7000
        assert config.LOG_LEVEL == "WARNING"
        assert config.CHROMA_DB_DIR == "env/chromadb"
        assert config.VAULT_PATH == "env/vault"
        assert config.VAULT_INDEX_BATCH_SIZE == 200
        
    finally:
        # Clean up environment variables
        for key in env_vars:
            del os.environ[key]


def test_invalid_config_file(tmp_path):
    """Test handling of invalid YAML configuration file."""
    config_file = tmp_path / "invalid.yaml"
    config_file.write_text("invalid: yaml: content")
    
    with pytest.raises(yaml.YAMLError):
        load_config(str(config_file))


def test_nonexistent_config_file():
    """Test handling of nonexistent configuration file."""
    with pytest.raises(FileNotFoundError):
        load_config("/nonexistent/config.yaml")


def test_empty_config_file(tmp_path):
    """Test handling of empty configuration file."""
    config_file = tmp_path / "empty.yaml"
    config_file.touch()
    
    config = load_config(str(config_file))
    assert isinstance(config, AppConfig)
    # Should use default values
    assert config.HOST == "127.0.0.1"
    assert config.PORT == 8000 