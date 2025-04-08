"""
Search service for Obsidian Concierge.

This module provides search functionality using vector embeddings.
"""

from typing import List, Optional, Dict, Any
from ..repository.chroma import ChromaRepository

class SearchService:
    """Service for handling vector-based search operations."""
    
    def __init__(self, repository: ChromaRepository):
        """
        Initialize SearchService.
        
        Args:
            repository: ChromaRepository instance for vector operations
        """
        self.repository = repository
    
    async def search(
        self,
        query: str,
        limit: Optional[int] = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for documents using vector similarity.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            filters: Optional metadata filters to apply
            
        Returns:
            List of documents with their metadata and similarity scores
            
        Raises:
            ValueError: If query is empty or invalid
            Exception: If search operation fails
        """
        if not query.strip():
            raise ValueError("Search query cannot be empty")
            
        try:
            # Get vector embedding for query
            results = await self.repository.search(
                query=query,
                limit=limit,
                filters=filters or {}
            )
            
            # Process and format results
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": float(score)  # Convert to float for JSON serialization
                })
                
            return formatted_results
            
        except Exception as e:
            raise Exception(f"Search failed: {str(e)}")
            
    async def get_similar_documents(
        self,
        document_id: str,
        limit: Optional[int] = 5
    ) -> List[Dict[str, Any]]:
        """
        Find documents similar to a given document.
        
        Args:
            document_id: ID of the document to find similar ones for
            limit: Maximum number of similar documents to return
            
        Returns:
            List of similar documents with their metadata and similarity scores
            
        Raises:
            ValueError: If document_id is invalid
            Exception: If similarity search fails
        """
        if not document_id.strip():
            raise ValueError("Document ID cannot be empty")
            
        try:
            results = await self.repository.find_similar(
                document_id=document_id,
                limit=limit
            )
            
            # Process and format results
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": float(score)
                })
                
            return formatted_results
            
        except Exception as e:
            raise Exception(f"Similarity search failed: {str(e)}") 