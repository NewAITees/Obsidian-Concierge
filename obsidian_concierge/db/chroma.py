"""
ChromaDB repository implementation for vector search functionality.

This module provides a wrapper around ChromaDB for document storage and retrieval.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging
import chromadb
from chromadb.config import Settings

logger = logging.getLogger(__name__)

@dataclass
class Document:
    """Represents a document in the vector store."""
    id: str
    content: str
    metadata: Dict[str, Any]

class ChromaRepository:
    """Repository for managing document vectors using ChromaDB."""
    
    def __init__(
        self,
        collection_name: str,
        persist_directory: str = ".chroma",
        embedding_function = None  # Will use default if None
    ):
        """Initialize ChromaDB repository.
        
        Args:
            collection_name: Name of the ChromaDB collection
            persist_directory: Directory to persist vectors
            embedding_function: Optional custom embedding function
        """
        self.collection_name = collection_name
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False
            )
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_function
        )
        
        logger.info(f"Initialized ChromaRepository with collection '{collection_name}'")
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store.
        
        Args:
            documents: List of Document objects to add
        """
        if not documents:
            return
            
        try:
            # Prepare data for ChromaDB
            ids = [doc.id for doc in documents]
            contents = [doc.content for doc in documents]
            metadatas = [doc.metadata for doc in documents]
            
            # Add to collection
            self.collection.add(
                ids=ids,
                documents=contents,
                metadatas=metadatas
            )
            
            logger.info(f"Added {len(documents)} documents to collection")
            
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise
    
    def query(
        self,
        query_text: str,
        n_results: int = 10,
        where: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """Query the vector store for similar documents.
        
        Args:
            query_text: Text to search for
            n_results: Maximum number of results to return
            where: Optional metadata filter conditions
            
        Returns:
            List of matching Document objects
        """
        try:
            # Execute query
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results,
                where=where
            )
            
            # Convert results to Document objects
            documents = []
            for i in range(len(results["ids"][0])):
                doc = Document(
                    id=results["ids"][0][i],
                    content=results["documents"][0][i],
                    metadata=results["metadatas"][0][i] if results["metadatas"] else {}
                )
                documents.append(doc)
            
            logger.info(f"Found {len(documents)} documents for query: {query_text}")
            return documents
            
        except Exception as e:
            logger.error(f"Error querying documents: {str(e)}")
            raise
    
    def delete_documents(self, ids: List[str]) -> None:
        """Delete documents from the vector store.
        
        Args:
            ids: List of document IDs to delete
        """
        try:
            self.collection.delete(ids=ids)
            logger.info(f"Deleted {len(ids)} documents")
        except Exception as e:
            logger.error(f"Error deleting documents: {str(e)}")
            raise
    
    def update_document(self, document: Document) -> None:
        """Update a document in the vector store.
        
        Args:
            document: Document object with updated content/metadata
        """
        try:
            self.collection.update(
                ids=[document.id],
                documents=[document.content],
                metadatas=[document.metadata]
            )
            logger.info(f"Updated document {document.id}")
        except Exception as e:
            logger.error(f"Error updating document: {str(e)}")
            raise 