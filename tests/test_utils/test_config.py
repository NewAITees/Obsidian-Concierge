"""
Tests for configuration management utilities.
"""

import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest
import yaml

from obsidian_concierge.utils.config import AppConfig, load_config


def test_default_config():
    """Test loading default configuration."""
    config = load_config()
    assert isinstance(config, AppConfig)
    assert config.HOST == "0.0.0.0"
    assert config.PORT == 8000
    assert config.LOG_LEVEL == "INFO"


def test_config_from_yaml():
    """Test loading configuration from YAML file."""
    test_config = {
        "HOST": "localhost",
        "PORT": 9000,
        "LOG_LEVEL": "DEBUG"
    }
    
    with NamedTemporaryFile(mode="w", suffix=".yaml") as f:
        yaml.dump(test_config, f)
        f.flush()
        
        config = load_config(f.name)
        assert config.HOST == "localhost"
        assert config.PORT == 9000
        assert config.LOG_LEVEL == "DEBUG"


def test_config_from_env():
    """Test loading configuration from environment variables."""
    os.environ["HOST"] = "127.0.0.1"
    os.environ["PORT"] = "5000"
    os.environ["LOG_LEVEL"] = "WARNING"
    
    try:
        config = load_config()
        assert config.HOST == "127.0.0.1"
        assert config.PORT == 5000
        assert config.LOG_LEVEL == "WARNING"
    finally:
        # Clean up environment variables
        del os.environ["HOST"]
        del os.environ["PORT"]
        del os.environ["LOG_LEVEL"]


def test_invalid_config_file():
    """Test handling of invalid configuration file."""
    with NamedTemporaryFile(mode="w", suffix=".yaml") as f:
        f.write("invalid: yaml: content:")
        f.flush()
        
        with pytest.raises(yaml.YAMLError):
            load_config(f.name)


def test_nonexistent_config_file():
    """Test handling of nonexistent configuration file."""
    with pytest.raises(FileNotFoundError):
        load_config("/nonexistent/config.yaml") 