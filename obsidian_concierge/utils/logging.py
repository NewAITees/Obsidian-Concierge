"""
Logging configuration for the application.

This module provides a centralized logging configuration for the entire application.
It sets up logging with proper formatting, handlers, and log levels based on the
environment configuration.
"""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class LogConfig(BaseModel):
    """Configuration model for logging settings."""
    
    LOGGER_NAME: str = "obsidian_concierge"
    LOG_FORMAT: str = "%(levelname)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = None
    LOG_FILE_MAX_BYTES: int = 10 * 1024 * 1024  # 10MB
    LOG_FILE_BACKUP_COUNT: int = 5


def setup_logging(config: LogConfig) -> logging.Logger:
    """
    Set up logging configuration for the application.
    
    Args:
        config: LogConfig instance containing logging configuration
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(config.LOGGER_NAME)
    logger.setLevel(config.LOG_LEVEL)

    # Create formatter
    formatter = logging.Formatter(config.LOG_FORMAT)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (if log file is specified)
    if config.LOG_FILE:
        log_dir = Path(config.LOG_FILE).parent
        if not log_dir.exists():
            log_dir.mkdir(parents=True)
            
        file_handler = logging.handlers.RotatingFileHandler(
            config.LOG_FILE,
            maxBytes=config.LOG_FILE_MAX_BYTES,
            backupCount=config.LOG_FILE_BACKUP_COUNT
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Default logger instance
logger = setup_logging(LogConfig()) 