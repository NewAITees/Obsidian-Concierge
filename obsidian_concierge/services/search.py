"""
Search service.

This module provides functionality for searching the indexed vault content.
"""

from typing import List, Optional, Dict, Any

from ..repository.chroma import ChromaRepository

class SearchService:
    """Search service."""
    
    def __init__(self, repo: ChromaRepository):
        """Initialize the service."""
        self.repo = repo
    
    async def search(
        self,
        query: str,
        limit: Optional[int] = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search the indexed vault content.
        
        Args:
            query: Search query
            limit: Maximum number of results to return
            filters: Optional filters to apply
            
        Returns:
            List of search results
        """
        results = await self.repo.search(
            query=query,
            limit=limit,
            filters=filters
        )
        return results

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
            results = await self.repo.find_similar(
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