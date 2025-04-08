"""
Question Answering service for Obsidian Concierge.

This module provides question answering functionality using LLMs and vector search.
"""

from typing import List, Optional, Dict, Any, Tuple
from ..repository.chroma import ChromaRepository
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

class QAService:
    """Service for handling question answering operations."""
    
    def __init__(self, repository: ChromaRepository):
        """
        Initialize QAService.
        
        Args:
            repository: ChromaRepository instance for context retrieval
        """
        self.repository = repository
        self.llm = ChatOpenAI(
            model_name="gpt-4-turbo-preview",
            temperature=0.7
        )
        
        # Define QA prompt template
        self.qa_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful assistant that answers questions based on the provided context.
            Use only the information from the context to answer the question.
            If you cannot find the answer in the context, say so.
            Always cite your sources using the metadata provided."""),
            ("user", "Context:\n{context}\n\nQuestion: {question}")
        ])
        
        self.qa_chain = LLMChain(
            llm=self.llm,
            prompt=self.qa_prompt
        )
    
    async def get_answer(
        self,
        question: str,
        context_size: Optional[int] = 3,
        temperature: Optional[float] = 0.7
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Answer a question using retrieved context.
        
        Args:
            question: Question to answer
            context_size: Number of documents to use as context
            temperature: LLM temperature for answer generation
            
        Returns:
            Tuple of (answer, context_documents)
            
        Raises:
            ValueError: If question is empty or invalid
            Exception: If QA operation fails
        """
        if not question.strip():
            raise ValueError("Question cannot be empty")
            
        try:
            # Get relevant context
            context_docs = await self.repository.search(
                query=question,
                limit=context_size
            )
            
            # Format context for prompt
            context_text = "\n\n".join([
                f"Document {i+1}:\n{doc.page_content}\nSource: {doc.metadata.get('source', 'Unknown')}"
                for i, (doc, _) in enumerate(context_docs)
            ])
            
            # Update LLM temperature
            self.llm.temperature = temperature
            
            # Generate answer
            response = await self.qa_chain.arun(
                context=context_text,
                question=question
            )
            
            # Format context documents for return
            formatted_context = []
            for doc, score in context_docs:
                formatted_context.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": float(score)
                })
            
            return response.strip(), formatted_context
            
        except Exception as e:
            raise Exception(f"Question answering failed: {str(e)}")
            
    async def get_follow_up_questions(
        self,
        question: str,
        answer: str,
        context: List[Dict[str, Any]],
        num_questions: Optional[int] = 3
    ) -> List[str]:
        """
        Generate follow-up questions based on the previous Q&A.
        
        Args:
            question: Original question
            answer: Generated answer
            context: Context documents used
            num_questions: Number of follow-up questions to generate
            
        Returns:
            List of follow-up questions
            
        Raises:
            ValueError: If inputs are invalid
            Exception: If generation fails
        """
        if not all([question.strip(), answer.strip(), context]):
            raise ValueError("All inputs must be non-empty")
            
        try:
            # Create prompt for follow-up questions
            followup_prompt = ChatPromptTemplate.from_messages([
                ("system", """Generate {num_questions} relevant follow-up questions based on the previous question, 
                answer, and context. The questions should explore related topics or dig deeper into specific aspects.
                Return only the questions, one per line."""),
                ("user", """Previous Question: {question}
                Answer: {answer}
                Context: {context}""")
            ])
            
            followup_chain = LLMChain(
                llm=self.llm,
                prompt=followup_prompt
            )
            
            # Format context
            context_text = "\n".join([
                doc["content"] for doc in context
            ])
            
            # Generate questions
            response = await followup_chain.arun(
                question=question,
                answer=answer,
                context=context_text,
                num_questions=num_questions
            )
            
            # Parse response into list
            questions = [q.strip() for q in response.strip().split("\n") if q.strip()]
            return questions[:num_questions]
            
        except Exception as e:
            raise Exception(f"Follow-up question generation failed: {str(e)}") 