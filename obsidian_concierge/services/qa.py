"""
Question answering service.

This module provides functionality for answering questions using the indexed vault content.
"""

from typing import List, Optional, Tuple

from ..repository.chroma import ChromaRepository
from ..llm.ollama import OllamaClient

class QAService:
    """Question answering service."""
    
    def __init__(self, repo: ChromaRepository):
        """Initialize the service."""
        self.repo = repo
        self.llm = OllamaClient()
    
    async def answer_question(
        self,
        question: str,
        context_size: Optional[int] = 3,
        temperature: Optional[float] = 0.7
    ) -> Tuple[str, List[dict], float]:
        """
        Answer a question using the indexed vault content.
        
        Args:
            question: Question to answer
            context_size: Number of context documents to use
            temperature: Temperature for response generation
            
        Returns:
            Tuple of (answer, context, confidence)
        """
        # Get relevant context from repository
        context = await self.repo.search(
            query=question,
            limit=context_size
        )
        
        # Format context for LLM
        context_text = "\n\n".join([
            f"Document: {doc['metadata']['title']}\n{doc['text']}"
            for doc in context
        ])
        
        # Generate answer
        prompt = f"""Based on the following context, answer the question.
        If you cannot answer the question based on the context, say so.
        
        Context:
        {context_text}
        
        Question: {question}
        
        Answer:"""
        
        answer = await self.llm.generate(
            prompt=prompt,
            temperature=temperature
        )
        
        # Simple confidence score based on context relevance
        confidence = 0.8  # TODO: Implement proper confidence scoring
        
        return answer, context, confidence

    async def get_follow_up_questions(
        self,
        question: str,
        answer: str,
        context: List[dict],
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
                doc["text"] for doc in context
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