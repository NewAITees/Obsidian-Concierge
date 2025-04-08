"""
Ollama client implementation.

This module provides a client for interacting with the Ollama API.
"""

import json
from typing import Optional, Dict, Any, List
import logging
import httpx
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class GenerateRequest(BaseModel):
    """Request model for text generation."""
    model: str
    prompt: str
    system: Optional[str] = None
    template: Optional[str] = None
    context: Optional[List[int]] = None
    options: Optional[Dict[str, Any]] = None
    stream: bool = False

class OllamaClient:
    """Client for interacting with Ollama API."""
    
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "gemma3:27b",
        timeout: float = 30.0
    ):
        """Initialize Ollama client.
        
        Args:
            base_url: Ollama API base URL
            model: Default model to use
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.api_url = f"{self.base_url}/api"
        
        logger.info(f"Initialized OllamaClient with model {model}")
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stop: Optional[List[str]] = None,
        template: Optional[str] = None,
        context: Optional[List[int]] = None
    ) -> str:
        """Generate text using the Ollama model.
        
        Args:
            prompt: Input text prompt
            system_prompt: Optional system prompt for context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            stop: Optional list of stop sequences
            template: Optional custom prompt template
            context: Optional context window
            
        Returns:
            Generated text response
        """
        try:
            # Prepare request data
            options = {
                "temperature": temperature,
            }
            if max_tokens:
                options["num_predict"] = max_tokens
            if stop:
                options["stop"] = stop
            
            request = GenerateRequest(
                model=self.model,
                prompt=prompt,
                system=system_prompt,
                template=template,
                context=context,
                options=options
            )
            
            logger.debug(f"Generate request: {request.dict()}")
            
            # Make API request
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/generate",
                    json=request.dict(exclude_none=True),
                    timeout=self.timeout
                )
                response.raise_for_status()
                
                result = response.json()
                logger.debug(f"Generate response: {result}")
                
                return result.get("response", "")
                
        except httpx.TimeoutException:
            logger.error("Ollama request timed out")
            raise
        except httpx.HTTPError as e:
            logger.error(f"Ollama HTTP error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Ollama generate error: {str(e)}")
            raise
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """Generate a chat response.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated response text
        """
        try:
            # Format chat history into prompt
            prompt = ""
            if system_prompt:
                prompt += f"System: {system_prompt}\n\n"
            
            for msg in messages:
                role = msg["role"].capitalize()
                content = msg["content"]
                prompt += f"{role}: {content}\n\n"
            
            prompt += "Assistant: "
            
            # Generate response
            response = await self.generate(
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Chat error: {str(e)}")
            raise
    
    async def embed(
        self,
        text: str,
        model: Optional[str] = None
    ) -> List[float]:
        """Generate embeddings for text.
        
        Args:
            text: Input text to embed
            model: Optional specific model to use
            
        Returns:
            List of embedding values
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/embeddings",
                    json={
                        "model": model or self.model,
                        "prompt": text
                    },
                    timeout=self.timeout
                )
                response.raise_for_status()
                
                result = response.json()
                return result.get("embedding", [])
        except Exception as e:
            logger.error(f"Embed error: {str(e)}")
            raise 