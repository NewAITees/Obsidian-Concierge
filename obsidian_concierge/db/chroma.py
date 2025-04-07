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
import re

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

    def _convert_metadata_for_storage(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Convert metadata to a format suitable for storage in ChromaDB."""
        if not metadata:
            return {}

        converted_metadata = metadata.copy()
        if "tags" in converted_metadata:
            tags = converted_metadata["tags"]
            if isinstance(tags, list):
                # Store each tag as a separate boolean field with index for order
                for i, tag in enumerate(tags):
                    converted_metadata[f"tag_{i}_{tag}"] = True
            else:
                # If a single tag is provided, store it as a boolean field
                converted_metadata[f"tag_0_{str(tags)}"] = True
            # Remove the original tags field
            del converted_metadata["tags"]
            logger.debug(f"Converted metadata for storage: {converted_metadata}")

        return converted_metadata

    def _convert_metadata_from_storage(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Convert metadata from storage format to application format."""
        if not metadata:
            return {}

        converted_metadata = metadata.copy()
        # Extract tags from boolean fields
        tag_fields = [(k, int(k.split('_')[1])) for k in converted_metadata.keys() if k.startswith("tag_")]
        if tag_fields:
            # Sort by index to preserve original order
            tag_fields.sort(key=lambda x: x[1])
            tags = []
            for field, _ in tag_fields:
                if converted_metadata[field]:  # Only include if True
                    tag = '_'.join(field.split('_')[2:])  # Remove 'tag_N_' prefix
                    tags.append(tag)
                del converted_metadata[field]
            
            converted_metadata["tags"] = tags
            logger.debug(f"Converted metadata from storage: {converted_metadata}")

        return converted_metadata
    
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
        metadatas = [self._convert_metadata_for_storage(doc.metadata) for doc in documents]
        
        logger.debug(f"Adding documents with metadatas: {metadatas}")
        
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
        n_results: int = 10,
        where: Optional[Dict[str, Any]] = None,
    ) -> List[Document]:
        """Query documents by similarity and optional metadata filters."""
        try:
            # Handle tag filtering
            if where and "tags" in where:
                tags = where["tags"]
                if isinstance(tags, list):
                    # For a list of tags, create a filter that matches any of the tags
                    conditions = []
                    for i, tag in enumerate(tags):
                        # Try each position for the tag
                        conditions.append({f"tag_{i}_{tag}": True})
                    where = {"$or": conditions}
                else:
                    # For a single tag, try it in position 0
                    where = {f"tag_0_{str(tags)}": True}
                logger.debug(f"Modified where condition: {where}")

            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results,
                where=where,
            )
            logger.debug(f"Query results: {results}")

            documents = []
            for i in range(len(results["ids"][0])):
                doc_id = results["ids"][0][i]
                doc_content = results["documents"][0][i]
                doc_metadata = results["metadatas"][0][i]
                doc_metadata = self._convert_metadata_from_storage(doc_metadata)
                documents.append(Document(id=doc_id, content=doc_content, metadata=doc_metadata))

            return documents
        except Exception as e:
            logger.error(f"Error querying documents: {e}")
            raise
    
    def update_document(self, document: Document) -> None:
        """
        Update an existing document.
        
        Args:
            document: Document to update
        """
        metadata = self._convert_metadata_for_storage(document.metadata)
        logger.debug(f"Updating document {document.id} with metadata: {metadata}")
        
        self.collection.update(
            ids=[document.id],
            documents=[document.content],
            metadatas=[metadata]
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
                metadata = self._convert_metadata_from_storage(result["metadatas"][0])
                logger.debug(f"Retrieved document {id} with metadata: {metadata}")
                
                return Document(
                    id=id,
                    content=result["documents"][0],
                    metadata=metadata
                )
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving document {id}: {e}")
            return None 