"""
Search service implementation.

This module provides the core search functionality using the ChromaDB repository.
"""

from typing import List, Optional, Dict, Any
import logging
from pydantic import BaseModel

from ..db.chroma import ChromaRepository, Document

logger = logging.getLogger(__name__)

class SearchResult(BaseModel):
    """Search result model."""
    id: str
    title: str
    path: str
    excerpt: str
    relevance: float = 1.0

class SearchService:
    """Service for searching documents in the vault."""
    
    def __init__(self, repository: ChromaRepository):
        """Initialize search service.
        
        Args:
            repository: ChromaRepository instance for vector search
        """
        self.repository = repository
    
    async def search(
        self,
        query: str,
        limit: Optional[int] = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """Search for documents matching the query.
        
        Args:
            query: Search query text
            limit: Maximum number of results to return
            filters: Optional metadata filters
            
        Returns:
            List of SearchResult objects
        """
        logger.info(f"Searching for: {query} (limit={limit}, filters={filters})")
        
        try:
            # Convert filters to ChromaDB format
            where_condition = self._convert_filters(filters) if filters else None
            
            # Execute search
            documents = self.repository.query(
                query_text=query,
                n_results=limit,
                where=where_condition
            )
            
            # Convert to search results
            results = []
            for doc in documents:
                # Create excerpt (first 200 characters)
                excerpt = doc.content[:200] + "..." if len(doc.content) > 200 else doc.content
                
                # Get title from metadata or use filename
                title = doc.metadata.get("title", doc.metadata.get("filename", "Untitled"))
                
                result = SearchResult(
                    id=doc.id,
                    title=title,
                    path=doc.metadata.get("path", ""),
                    excerpt=excerpt,
                    relevance=0.9  # TODO: Use actual relevance score from ChromaDB
                )
                results.append(result)
            
            logger.info(f"Found {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            raise
    
    def _convert_filters(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Convert API filters to ChromaDB where conditions.
        
        Args:
            filters: Dictionary of filter conditions
            
        Returns:
            ChromaDB compatible where conditions
        """
        where = {}
        
        # Handle tag filters
        if "tags" in filters:
            tags = filters["tags"]
            if isinstance(tags, str):
                tags = [tags]
            where["tags"] = {"$in": tags}
        
        # Handle folder filters
        if "folder" in filters:
            folder = filters["folder"]
            where["path"] = {"$contains": folder}
        
        # Handle date filters
        if "created_after" in filters:
            where["created_at"] = {"$gte": filters["created_after"]}
        if "created_before" in filters:
            where["created_at"] = {"$lte": filters["created_before"]}
        
        # Pass through any other metadata filters
        for key, value in filters.items():
            if key not in ["tags", "folder", "created_after", "created_before"]:
                where[key] = value
        
        return where 