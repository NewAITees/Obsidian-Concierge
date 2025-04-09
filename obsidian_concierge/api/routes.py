"""
API routes for Obsidian Concierge.

This module defines the API endpoints for search and Q&A functionality.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from ..services.search import SearchService
from ..services.qa import QAService
from ..repository.chroma import ChromaRepository

# Initialize router
router = APIRouter()

# Initialize services
repo = ChromaRepository(collection_name="obsidian_vault")
search_service = SearchService(repo)
qa_service = QAService(repo)

class SearchRequest(BaseModel):
    """Search request model."""
    query: str = Field(..., description="Search query string")
    limit: Optional[int] = Field(10, description="Maximum number of results to return")
    filters: Optional[dict] = Field(None, description="Optional filters to apply")

class SearchResponse(BaseModel):
    """Search response model."""
    results: List[dict] = Field(..., description="List of search results")
    total: int = Field(..., description="Total number of results found")

class QuestionRequest(BaseModel):
    """Question request model."""
    question: str = Field(..., description="Question to answer")
    context_size: Optional[int] = Field(3, description="Number of context documents to use")
    temperature: Optional[float] = Field(0.7, description="Temperature for response generation")

class QuestionResponse(BaseModel):
    """Question response model."""
    answer: str = Field(..., description="Generated answer")
    context: List[dict] = Field(..., description="Context used to generate answer")
    confidence: float = Field(..., description="Confidence score of the answer")

@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest) -> SearchResponse:
    """
    Search endpoint that processes search requests.
    
    Args:
        request: SearchRequest object containing search parameters
        
    Returns:
        SearchResponse object containing search results
        
    Raises:
        HTTPException: If search fails
    """
    try:
        results = await search_service.search(
            query=request.query,
            limit=request.limit,
            filters=request.filters
        )
        return SearchResponse(
            results=results,
            total=len(results)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )

@router.post("/ask", response_model=QuestionResponse)
async def ask(request: QuestionRequest) -> QuestionResponse:
    """
    Question answering endpoint that processes questions.
    
    Args:
        request: QuestionRequest object containing the question and parameters
        
    Returns:
        QuestionResponse object containing the answer and context
        
    Raises:
        HTTPException: If question answering fails
    """
    try:
        answer, context, confidence = await qa_service.answer_question(
            question=request.question,
            context_size=request.context_size,
            temperature=request.temperature
        )
        return QuestionResponse(
            answer=answer,
            context=context,
            confidence=confidence
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Question answering failed: {str(e)}"
        ) 