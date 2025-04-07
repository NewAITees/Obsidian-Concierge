"""
Tests for vault indexer implementation.
"""

import os
import pytest
from pathlib import Path
from typing import Generator
from unittest.mock import Mock, patch

from obsidian_concierge.db.chroma import ChromaRepository, Document
from obsidian_concierge.indexer.vault_indexer import VaultIndexer


@pytest.fixture
def mock_repo():
    """Fixture for mock ChromaRepository."""
    return Mock(spec=ChromaRepository)


@pytest.fixture
def temp_vault(tmp_path):
    """Fixture for temporary vault directory with sample files."""
    vault_dir = tmp_path / "test_vault"
    vault_dir.mkdir()
    
    # Create some test markdown files
    files = [
        ("note1.md", "# Test Note 1\nThis is a test note."),
        ("folder1/note2.md", "# Test Note 2\nThis is another test note."),
        ("folder1/note3.md", "# Test Note 3\nYet another test note."),
        ("not_markdown.txt", "This is not a markdown file.")
    ]
    
    for file_path, content in files:
        file_path = vault_dir / file_path
        file_path.parent.mkdir(exist_ok=True)
        file_path.write_text(content)
    
    return vault_dir


def test_vault_indexer_initialization(temp_vault, mock_repo):
    """Test VaultIndexer initialization."""
    indexer = VaultIndexer(str(temp_vault), mock_repo)
    assert indexer.vault_path == temp_vault
    assert indexer.repo == mock_repo


def test_vault_indexer_invalid_path(mock_repo):
    """Test VaultIndexer initialization with invalid path."""
    with pytest.raises(ValueError):
        VaultIndexer("/nonexistent/path", mock_repo)


def test_read_markdown_file(temp_vault, mock_repo):
    """Test reading markdown file content."""
    indexer = VaultIndexer(str(temp_vault), mock_repo)
    content = indexer._read_markdown_file(temp_vault / "note1.md")
    assert content == "# Test Note 1\nThis is a test note."


def test_generate_document_id(temp_vault, mock_repo):
    """Test document ID generation."""
    indexer = VaultIndexer(str(temp_vault), mock_repo)
    file_path = temp_vault / "note1.md"
    doc_id = indexer._generate_document_id(file_path)
    
    # ID should be consistent for the same path
    assert doc_id == indexer._generate_document_id(file_path)
    
    # Different paths should have different IDs
    other_path = temp_vault / "folder1/note2.md"
    assert doc_id != indexer._generate_document_id(other_path)


def test_get_file_metadata(temp_vault, mock_repo):
    """Test file metadata extraction."""
    indexer = VaultIndexer(str(temp_vault), mock_repo)
    file_path = temp_vault / "note1.md"
    metadata = indexer._get_file_metadata(file_path)
    
    assert metadata["path"] == "note1.md"
    assert metadata["filename"] == "note1.md"
    assert metadata["extension"] == ".md"
    assert "created_at" in metadata
    assert "modified_at" in metadata
    assert "size_bytes" in metadata


def test_scan_vault_files(temp_vault, mock_repo):
    """Test scanning vault for markdown files."""
    indexer = VaultIndexer(str(temp_vault), mock_repo)
    files = list(indexer._scan_vault_files())
    
    # Should find 3 markdown files
    assert len(files) == 3
    assert all(f.suffix == ".md" for f in files)
    
    # Check specific files
    file_paths = {str(f.relative_to(temp_vault)) for f in files}
    assert file_paths == {"note1.md", "folder1/note2.md", "folder1/note3.md"}


def test_index_vault(temp_vault, mock_repo):
    """Test indexing entire vault."""
    indexer = VaultIndexer(str(temp_vault), mock_repo)
    indexer.index_vault(batch_size=2)
    
    # Check that add_documents was called with correct number of documents
    calls = mock_repo.add_documents.call_args_list
    total_docs = sum(len(args[0][0]) for args in calls)
    assert total_docs == 3  # Should have processed 3 markdown files


def test_reindex_file(temp_vault, mock_repo):
    """Test reindexing a single file."""
    indexer = VaultIndexer(str(temp_vault), mock_repo)
    file_path = temp_vault / "note1.md"
    
    indexer.reindex_file(str(file_path))
    
    # Check that update_document was called with correct document
    mock_repo.update_document.assert_called_once()
    doc = mock_repo.update_document.call_args[0][0]
    assert doc.content == "# Test Note 1\nThis is a test note."
    assert doc.metadata["path"] == "note1.md"


def test_remove_file(temp_vault, mock_repo):
    """Test removing a file from index."""
    indexer = VaultIndexer(str(temp_vault), mock_repo)
    file_path = temp_vault / "note1.md"
    
    indexer.remove_file(str(file_path))
    
    # Check that delete_documents was called with correct ID
    mock_repo.delete_documents.assert_called_once()
    doc_id = indexer._generate_document_id(file_path)
    assert mock_repo.delete_documents.call_args[0][0] == [doc_id]


def test_error_handling(temp_vault, mock_repo):
    """Test error handling during indexing."""
    indexer = VaultIndexer(str(temp_vault), mock_repo)
    
    # Simulate error during document addition
    mock_repo.add_documents.side_effect = Exception("Test error")
    
    with pytest.raises(Exception):
        indexer.index_vault()
    
    # Should still attempt to add any documents in the current batch
    assert mock_repo.add_documents.called 