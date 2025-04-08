"""
Question answering service implementation.

This module provides functionality for answering questions using the vault content.
"""

from typing import List, Optional, Dict, Any
import logging
from pydantic import BaseModel

from ..db.chroma import ChromaRepository
from ..llm.ollama import OllamaClient

logger = logging.getLogger(__name__)

class Source(BaseModel):
    """Source document reference."""
    id: str
    title: str
    path: str

class QuestionResponse(BaseModel):
    """Response model for question answering."""
    answer: str
    sources: List[Source]
    confidence: float = 1.0

class QAService:
    """Service for answering questions using vault content."""
    
    def __init__(
        self,
        repository: ChromaRepository,
        llm_client: Optional[OllamaClient] = None
    ):
        """Initialize QA service.
        
        Args:
            repository: ChromaRepository instance for searching content
            llm_client: Optional OllamaClient instance (creates new if None)
        """
        self.repository = repository
        self.llm_client = llm_client or OllamaClient()
    
    async def answer_question(
        self,
        question: str,
        max_context_items: int = 3,
        temperature: float = 0.7
    ) -> QuestionResponse:
        """Answer a question using vault content.
        
        Args:
            question: Question to answer
            max_context_items: Maximum number of context documents to use
            temperature: LLM temperature parameter
            
        Returns:
            QuestionResponse with answer and sources
        """
        logger.info(f"Answering question: {question}")
        
        try:
            # Search for relevant documents
            documents = self.repository.query(
                query_text=question,
                n_results=max_context_items
            )
            
            if not documents:
                return QuestionResponse(
                    answer="I couldn't find any relevant information to answer your question.",
                    sources=[],
                    confidence=0.0
                )
            
            # Build context from documents
            context = self._build_context(documents)
            
            # Build prompt
            system_prompt = """You are a knowledgeable assistant helping users understand their Obsidian vault content.
            Answer questions based on the provided context. If you cannot find a clear answer in the context, say so.
            Always be truthful and cite your sources when possible."""
            
            prompt = f"""Context information:
            {context}
            
            Question: {question}
            
            Please provide a clear and concise answer based on the context above. If you can't find enough information to answer confidently, say so."""
            
            # Generate answer
            answer = await self.llm_client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=temperature
            )
            
            # Prepare sources
            sources = []
            for doc in documents:
                title = doc.metadata.get("title", doc.metadata.get("filename", "Untitled"))
                source = Source(
                    id=doc.id,
                    title=title,
                    path=doc.metadata.get("path", "")
                )
                sources.append(source)
            
            # Calculate confidence (simple heuristic based on number of sources)
            confidence = min(len(sources) / max_context_items, 1.0)
            
            return QuestionResponse(
                answer=answer,
                sources=sources,
                confidence=confidence
            )
            
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            raise
    
    def _build_context(self, documents: List[Any]) -> str:
        """Build context string from documents.
        
        Args:
            documents: List of Document objects
            
        Returns:
            Formatted context string
        """
        context_parts = []
        
        for i, doc in enumerate(documents, 1):
            title = doc.metadata.get("title", doc.metadata.get("filename", "Untitled"))
            context_parts.append(f"[Document {i}: {title}]\n{doc.content}\n")
        
        return "\n---\n".join(context_parts) 