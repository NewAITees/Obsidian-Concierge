"""
Tests for file system utilities.
"""

import os
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

import pytest

from obsidian_concierge.utils.fs import (ensure_dir, get_file_extension,
                                        get_file_size, is_text_file, list_files,
                                        safe_remove)


def test_ensure_dir():
    """Test directory creation."""
    with TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir) / "test" / "nested"
        result = ensure_dir(test_dir)
        
        assert result == test_dir
        assert test_dir.exists()
        assert test_dir.is_dir()


def test_list_files():
    """Test file listing."""
    with TemporaryDirectory() as temp_dir:
        # Create test files
        dir_path = Path(temp_dir)
        (dir_path / "test1.txt").touch()
        (dir_path / "test2.txt").touch()
        (dir_path / "test.md").touch()
        
        # Create nested directory with files
        nested_dir = dir_path / "nested"
        nested_dir.mkdir()
        (nested_dir / "nested1.txt").touch()
        
        # Test non-recursive listing
        files = list_files(dir_path, pattern="*.txt", recursive=False)
        assert len(files) == 2
        assert all(f.suffix == ".txt" for f in files)
        
        # Test recursive listing
        files = list_files(dir_path, pattern="*.txt", recursive=True)
        assert len(files) == 3
        assert all(f.suffix == ".txt" for f in files)


def test_safe_remove():
    """Test safe file and directory removal."""
    with TemporaryDirectory() as temp_dir:
        # Test file removal
        test_file = Path(temp_dir) / "test.txt"
        test_file.touch()
        safe_remove(test_file)
        assert not test_file.exists()
        
        # Test directory removal
        test_dir = Path(temp_dir) / "test_dir"
        test_dir.mkdir()
        (test_dir / "test.txt").touch()
        safe_remove(test_dir)
        assert not test_dir.exists()
        
        # Test non-existent path
        safe_remove(Path(temp_dir) / "nonexistent")  # Should not raise


def test_get_file_extension():
    """Test file extension extraction."""
    assert get_file_extension("test.txt") == "txt"
    assert get_file_extension("test.TXT") == "txt"
    assert get_file_extension("test") == ""
    assert get_file_extension(".gitignore") == "gitignore"
    assert get_file_extension("path/to/test.md") == "md"


def test_is_text_file():
    """Test text file detection."""
    with TemporaryDirectory() as temp_dir:
        # Test text file
        text_file = Path(temp_dir) / "test.txt"
        with open(text_file, "w") as f:
            f.write("Hello, world!")
        assert is_text_file(text_file)
        
        # Test binary file
        binary_file = Path(temp_dir) / "test.bin"
        with open(binary_file, "wb") as f:
            f.write(bytes(range(256)))
        assert not is_text_file(binary_file)


def test_get_file_size():
    """Test file size calculation."""
    with NamedTemporaryFile() as temp_file:
        # Write test content
        content = b"Hello, world!"
        temp_file.write(content)
        temp_file.flush()
        
        size = get_file_size(temp_file.name)
        assert size == len(content)
        
        # Test non-existent file
        with pytest.raises(FileNotFoundError):
            get_file_size("/nonexistent/file.txt") 