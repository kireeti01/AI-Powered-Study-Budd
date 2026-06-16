"""
Google Gemini API Client Utility
Handles all interactions with the Gemini API
"""

import google.generativeai as genai
from typing import Optional, List
import logging
from src.config.settings import Config, ERROR_MESSAGES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeminiClient:
    """
    Client for interacting with Google Gemini API
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini API Client
        
        Args:
            api_key: Google Gemini API key
            
        Raises:
            ValueError: If API key is not provided or invalid
        """
        self.api_key = api_key or Config.API_KEY
        
        if not self.api_key:
            raise ValueError(ERROR_MESSAGES["api_key_missing"])
        
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(Config.MODEL_NAME)
            logger.info("✅ Gemini API client initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini API: {str(e)}")
            raise ValueError(ERROR_MESSAGES["api_error"])
    
    def generate_text(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate text using Gemini API
        
        Args:
            prompt: User input prompt
            temperature: Creativity level (0.0 - 1.0)
            max_tokens: Maximum output tokens
            system_prompt: System instructions for the model
            
        Returns:
            Generated text response
            
        Raises:
            Exception: If API call fails
        """
        try:
            temperature = temperature or Config.TEMPERATURE
            max_tokens = max_tokens or Config.MAX_TOKENS
            
            # Prepare generation config
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                top_p=0.95,
                top_k=40,
            )
            
            # Build full prompt
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            # Generate response
            response = self.model.generate_content(
                full_prompt,
                generation_config=generation_config
            )
            
            if response and response.text:
                logger.info("✅ Successfully generated text from Gemini API")
                return response.text
            else:
                raise ValueError("Empty response from API")
                
        except Exception as e:
            logger.error(f"❌ API Error: {str(e)}")
            raise Exception(f"{ERROR_MESSAGES['api_error']}\nDetails: {str(e)}")
    
    def generate_structured_content(
        self,
        prompt: str,
        output_format: str = "json",
        temperature: Optional[float] = None
    ) -> dict:
        """
        Generate structured content (JSON, markdown, etc.)
        
        Args:
            prompt: User prompt
            output_format: Expected output format
            temperature: Creativity level
            
        Returns:
            Parsed structured response
        """
        try:
            # Add format instruction to prompt
            format_prompt = f"{prompt}\n\nProvide response in {output_format} format."
            
            response_text = self.generate_text(
                format_prompt,
                temperature=temperature or 0.5
            )
            
            # Parse response based on format
            if output_format.lower() == "json":
                import json
                # Extract JSON from response
                try:
                    return json.loads(response_text)
                except json.JSONDecodeError:
                    # Try to extract JSON from markdown code blocks
                    if "```json" in response_text:
                        json_str = response_text.split("```json")[1].split("```")[0]
                        return json.loads(json_str)
                    elif "```" in response_text:
                        json_str = response_text.split("```")[1].split("```")[0]
                        return json.loads(json_str)
                    return {"response": response_text}
            
            return {"response": response_text}
            
        except Exception as e:
            logger.error(f"❌ Failed to generate structured content: {str(e)}")
            return {"error": str(e)}
    
    def generate_with_context(
        self,
        prompt: str,
        context: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Generate text with provided context
        
        Args:
            prompt: User question/prompt
            context: Reference context/content
            system_prompt: System instructions
            temperature: Creativity level
            
        Returns:
            Generated response based on context
        """
        try:
            # Create context-aware prompt
            context_prompt = f"""Context/Reference Material:
{context}

User Query:
{prompt}

Please answer based on the provided context."""
            
            return self.generate_text(
                context_prompt,
                temperature=temperature or 0.5,
                system_prompt=system_prompt
            )
            
        except Exception as e:
            logger.error(f"❌ Failed to generate context-aware response: {str(e)}")
            raise
    
    def generate_batch(self, prompts: List[str]) -> List[str]:
        """
        Generate responses for multiple prompts
        
        Args:
            prompts: List of prompts
            
        Returns:
            List of generated responses
        """
        try:
            responses = []
            for prompt in prompts:
                response = self.generate_text(prompt)
                responses.append(response)
            
            logger.info(f"✅ Successfully generated {len(responses)} responses")
            return responses
            
        except Exception as e:
            logger.error(f"❌ Batch generation failed: {str(e)}")
            raise
    
    def verify_api_connection(self) -> bool:
        """
        Verify API connection is working
        
        Returns:
            True if connection is successful
        """
        try:
            response = self.generate_text("Say 'OK' in one word")
            return bool(response)
        except Exception as e:
            logger.error(f"❌ API connection verification failed: {str(e)}")
            return False


# Singleton instance for app-wide use
_gemini_client = None


def get_gemini_client() -> GeminiClient:
    """
    Get or create singleton Gemini client
    
    Returns:
        GeminiClient instance
    """
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = GeminiClient()
    return _gemini_client
