"""
File system utilities.

This module provides helper functions for common file system operations used
throughout the application.
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional, Set

from .logging import logger


def ensure_dir(path: str | Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path to ensure
        
    Returns:
        Path object of the ensured directory
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def list_files(
    directory: str | Path,
    pattern: str = "*",
    recursive: bool = True
) -> List[Path]:
    """
    List files in a directory matching a pattern.
    
    Args:
        directory: Directory to search in
        pattern: Glob pattern to match files against
        recursive: Whether to search recursively
        
    Returns:
        List of matching file paths
        
    Raises:
        FileNotFoundError: If directory doesn't exist
    """
    directory = Path(directory)
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
        
    if recursive:
        return list(directory.rglob(pattern))
    return list(directory.glob(pattern))


def safe_remove(path: str | Path) -> None:
    """
    Safely remove a file or directory.
    
    Args:
        path: Path to remove
    """
    path = Path(path)
    try:
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
    except Exception as e:
        logger.warning(f"Failed to remove {path}: {e}")


def get_file_extension(path: str | Path) -> str:
    """
    Get the extension of a file (lowercase).
    
    Args:
        path: File path
        
    Returns:
        Lowercase file extension without dot
    """
    return Path(path).suffix.lower().lstrip(".")


def is_text_file(path: str | Path, max_check_size: int = 8000) -> bool:
    """
    Check if a file appears to be a text file.
    
    Args:
        path: File path to check
        max_check_size: Maximum number of bytes to check
        
    Returns:
        True if file appears to be text, False otherwise
    """
    try:
        with open(path, "rb") as f:
            chunk = f.read(max_check_size)
            return not bool(chunk.translate(None, bytes(range(32, 127)) + b"\n\r\t\f\b"))
    except Exception:
        return False


def get_file_size(path: str | Path) -> int:
    """
    Get the size of a file in bytes.
    
    Args:
        path: Path to the file
        
    Returns:
        File size in bytes
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return path.stat().st_size 