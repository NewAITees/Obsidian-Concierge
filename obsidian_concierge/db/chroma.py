"""
Chromadb repository implementation.

This module provides a repository class for interacting with ChromaDB, handling
document storage, retrieval, and search operations.
"""

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from pydantic import BaseModel
from typing import List, Dict, Optional, Any

from ..utils.config import config
from ..utils.logging import logger


class Document(BaseModel):
    """Document model for ChromaDB storage."""
    
    id: str
    content: str
    metadata: Dict[str, Any]


class ChromaRepository:
    """Repository class for ChromaDB operations."""
    
    def __init__(self, collection_name: str = "obsidian_notes"):
        """
        Initialize ChromaDB repository.
        
        Args:
            collection_name: Name of the ChromaDB collection to use
        """
        self.client = chromadb.PersistentClient(
            path=config.CHROMA_DB_DIR,
            settings=Settings(
                anonymized_telemetry=False
            )
        )
        
        # Use default embedding function (all-MiniLM-L6-v2)
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function,
            metadata={"hnsw:space": "cosine"}  # Use cosine similarity
        )
        
        logger.info(f"Initialized ChromaDB repository with collection: {collection_name}")
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Add multiple documents to the collection.
        
        Args:
            documents: List of documents to add
        """
        if not documents:
            return
            
        # Prepare document data
        ids = [doc.id for doc in documents]
        contents = [doc.content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        
        # Add to collection
        self.collection.add(
            ids=ids,
            documents=contents,
            metadatas=metadatas
        )
        
        logger.info(f"Added {len(documents)} documents to ChromaDB")
    
    def query(
        self,
        query_text: str,
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Query documents by similarity.
        
        Args:
            query_text: Text to search for
            n_results: Number of results to return
            where: Filter conditions
            
        Returns:
            List of matching documents
        """
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
                metadata=results["metadatas"][0][i]
            )
            documents.append(doc)
        
        return documents
    
    def update_document(self, document: Document) -> None:
        """
        Update an existing document.
        
        Args:
            document: Document to update
        """
        self.collection.update(
            ids=[document.id],
            documents=[document.content],
            metadatas=[document.metadata]
        )
        
        logger.info(f"Updated document: {document.id}")
    
    def delete_documents(self, ids: List[str]) -> None:
        """
        Delete documents by their IDs.
        
        Args:
            ids: List of document IDs to delete
        """
        if not ids:
            return
            
        self.collection.delete(ids=ids)
        logger.info(f"Deleted {len(ids)} documents from ChromaDB")
    
    def get_document(self, id: str) -> Optional[Document]:
        """
        Get a document by its ID.
        
        Args:
            id: Document ID to retrieve
            
        Returns:
            Document if found, None otherwise
        """
        try:
            result = self.collection.get(
                ids=[id],
                include=["documents", "metadatas"]
            )
            
            if result["ids"]:
                return Document(
                    id=id,
                    content=result["documents"][0],
                    metadata=result["metadatas"][0]
                )
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving document {id}: {e}")
            return None 