"""
Tests for ChromaDB repository implementation.
"""

import pytest
from typing import List
import uuid

from obsidian_concierge.db.chroma import ChromaRepository, Document


@pytest.fixture
def chroma_repo():
    """Fixture for ChromaRepository instance."""
    repo = ChromaRepository(collection_name=f"test_collection_{uuid.uuid4()}")
    yield repo
    # Cleanup
    repo.collection.delete()


@pytest.fixture
def sample_documents() -> List[Document]:
    """Fixture for sample documents."""
    return [
        Document(
            id="doc1",
            content="This is a test document about Python programming.",
            metadata={"type": "note", "tags": ["python", "programming"]}
        ),
        Document(
            id="doc2",
            content="FastAPI is a modern web framework for building APIs.",
            metadata={"type": "note", "tags": ["python", "fastapi", "web"]}
        ),
        Document(
            id="doc3",
            content="ChromaDB is a vector database for AI applications.",
            metadata={"type": "note", "tags": ["database", "ai"]}
        )
    ]


def test_add_documents(chroma_repo: ChromaRepository, sample_documents: List[Document]):
    """Test adding documents to the repository."""
    # Add documents
    chroma_repo.add_documents(sample_documents)
    
    # Verify each document was added
    for doc in sample_documents:
        stored_doc = chroma_repo.get_document(doc.id)
        assert stored_doc is not None
        assert stored_doc.id == doc.id
        assert stored_doc.content == doc.content
        assert stored_doc.metadata == doc.metadata


def test_query_documents(chroma_repo: ChromaRepository, sample_documents: List[Document]):
    """Test querying documents by similarity."""
    # Add documents
    chroma_repo.add_documents(sample_documents)
    
    # Query for Python-related documents
    results = chroma_repo.query("Python programming", n_results=2)
    assert len(results) == 2
    assert any("Python programming" in doc.content for doc in results)
    
    # Query with metadata filter
    results = chroma_repo.query(
        "web",
        where={"tags": "fastapi"}
    )
    assert len(results) == 1
    assert "FastAPI" in results[0].content


def test_update_document(chroma_repo: ChromaRepository, sample_documents: List[Document]):
    """Test updating a document."""
    # Add documents
    chroma_repo.add_documents(sample_documents)
    
    # Update first document
    updated_doc = Document(
        id="doc1",
        content="Updated content about Python programming.",
        metadata={"type": "note", "tags": ["python", "programming", "updated"]}
    )
    chroma_repo.update_document(updated_doc)
    
    # Verify update
    stored_doc = chroma_repo.get_document("doc1")
    assert stored_doc is not None
    assert stored_doc.content == updated_doc.content
    assert stored_doc.metadata == updated_doc.metadata


def test_delete_documents(chroma_repo: ChromaRepository, sample_documents: List[Document]):
    """Test deleting documents."""
    # Add documents
    chroma_repo.add_documents(sample_documents)
    
    # Delete two documents
    chroma_repo.delete_documents(["doc1", "doc2"])
    
    # Verify deletions
    assert chroma_repo.get_document("doc1") is None
    assert chroma_repo.get_document("doc2") is None
    assert chroma_repo.get_document("doc3") is not None


def test_get_nonexistent_document(chroma_repo: ChromaRepository):
    """Test getting a nonexistent document."""
    assert chroma_repo.get_document("nonexistent") is None


def test_empty_operations(chroma_repo: ChromaRepository):
    """Test operations with empty inputs."""
    # These should not raise exceptions
    chroma_repo.add_documents([])
    chroma_repo.delete_documents([])
    
    results = chroma_repo.query("test")
    assert len(results) == 0 