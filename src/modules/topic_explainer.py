"""
Topic Explainer Module
Provides AI-powered explanations of topics in simple language
"""

import logging
from typing import Optional, Dict, List
from src.utils.gemini_client import get_gemini_client
from src.utils.text_processor import TextProcessor
from src.utils.validators import Validators

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TopicExplainer:
    """
    Explains topics in simple, beginner-friendly language with examples
    """
    
    DIFFICULTY_LEVELS = {
        "beginner": "very simple language suitable for beginners",
        "intermediate": "clear language with some technical terms",
        "advanced": "technical language for advanced learners"
    }
    
    def __init__(self):
        """Initialize Topic Explainer with Gemini client"""
        self.client = get_gemini_client()
        logger.info("✅ Topic Explainer initialized")
    
    def explain_topic(
        self,
        topic: str,
        difficulty: str = "beginner",
        include_examples: bool = True,
        include_applications: bool = True,
        max_length: str = "medium"
    ) -> Dict[str, str]:
        """
        Explain a topic with examples and applications
        
        Args:
            topic: Topic to explain
            difficulty: Level (beginner, intermediate, advanced)
            include_examples: Include real-world examples
            include_applications: Include practical applications
            max_length: Response length (short, medium, long)
            
        Returns:
            Dictionary with explanation components
            
        Raises:
            ValueError: If topic is invalid
        """
        try:
            # Validate input
            Validators.is_valid_topic(topic)
            
            if difficulty not in self.DIFFICULTY_LEVELS:
                raise ValueError(f"❌ Invalid difficulty level. Choose from: {list(self.DIFFICULTY_LEVELS.keys())}")
            
            logger.info(f"📚 Explaining topic: {topic} (difficulty: {difficulty})")
            
            # Build system prompt
            system_prompt = f"""You are an expert educator. Explain topics in {self.DIFFICULTY_LEVELS[difficulty]}.
            
Structure your explanation as follows:
1. SIMPLE DEFINITION: A clear, one-sentence definition
2. DETAILED EXPLANATION: Expand on the concept (2-3 paragraphs)
3. KEY CONCEPTS: List 3-5 important points
4. REAL-WORLD EXAMPLES: Provide relatable examples
5. PRACTICAL APPLICATIONS: How it's used in real life
6. COMMON MISCONCEPTIONS: What people often get wrong

Be engaging, clear, and avoid jargon where possible."""
            
            # Build user prompt
            user_prompt = f"Explain the topic '{topic}' in detail"
            
            if not include_examples:
                user_prompt += " (skip examples)"
            
            if not include_applications:
                user_prompt += " (skip applications)"
            
            # Generate explanation
            explanation = self.client.generate_text(
                user_prompt,
                system_prompt=system_prompt,
                temperature=0.7
            )
            
            # Parse response
            components = self._parse_explanation(explanation, topic)
            
            logger.info(f"✅ Successfully explained topic: {topic}")
            return components
            
        except Exception as e:
            logger.error(f"❌ Topic explanation failed: {str(e)}")
            raise
    
    def _parse_explanation(self, explanation: str, topic: str) -> Dict[str, str]:
        """
        Parse AI response into structured components
        
        Args:
            explanation: Raw explanation text
            topic: Original topic
            
        Returns:
            Dictionary with structured explanation
        """
        components = {
            "topic": topic,
            "full_explanation": explanation,
            "summary": TextProcessor.summarize_text(explanation, num_sentences=2),
            "key_phrases": TextProcessor.extract_key_phrases(explanation, num_phrases=5)
        }
        
        return components
    
    def explain_with_context(
        self,
        topic: str,
        context: str,
        difficulty: str = "beginner"
    ) -> Dict[str, str]:
        """
        Explain a topic with provided context
        
        Args:
            topic: Topic to explain
            context: Additional context or background
            difficulty: Difficulty level
            
        Returns:
            Dictionary with explanation
        """
        try:
            logger.info(f"📚 Explaining {topic} with context")
            
            # Validate inputs
            Validators.is_valid_topic(topic)
            
            system_prompt = f"""You are an expert educator. Explain the topic considering the provided context.
Use {self.DIFFICULTY_LEVELS[difficulty]}.

Structure your response:
1. How it relates to the context provided
2. Detailed explanation with examples
3. Key takeaways
4. Further learning points"""
            
            user_prompt = f"""Context: {context}

Please explain '{topic}' in relation to this context."""
            
            explanation = self.client.generate_text(
                user_prompt,
                system_prompt=system_prompt,
                temperature=0.7
            )
            
            return self._parse_explanation(explanation, topic)
            
        except Exception as e:
            logger.error(f"❌ Context-based explanation failed: {str(e)}")
            raise
    
    def compare_topics(self, topic1: str, topic2: str) -> Dict[str, str]:
        """
        Compare two topics and explain similarities and differences
        
        Args:
            topic1: First topic
            topic2: Second topic
            
        Returns:
            Dictionary with comparison
        """
        try:
            logger.info(f"🔍 Comparing: {topic1} vs {topic2}")
            
            # Validate inputs
            Validators.is_valid_topic(topic1)
            Validators.is_valid_topic(topic2)
            
            system_prompt = """You are an expert educator. Compare two concepts clearly.

Structure your response:
1. SIMILARITIES: What they have in common
2. DIFFERENCES: How they differ
3. WHEN TO USE: When to use each one
4. EXAMPLES: Real-world examples for each
5. LEARNING TIPS: Tips for understanding both"""
            
            user_prompt = f"""Compare and contrast these two topics:
Topic 1: {topic1}
Topic 2: {topic2}

Provide a detailed comparison."""
            
            comparison = self.client.generate_text(
                user_prompt,
                system_prompt=system_prompt,
                temperature=0.7
            )
            
            return {
                "topic1": topic1,
                "topic2": topic2,
                "comparison": comparison,
                "summary": TextProcessor.summarize_text(comparison, num_sentences=3)
            }
            
        except Exception as e:
            logger.error(f"❌ Topic comparison failed: {str(e)}")
            raise
    
    def explain_step_by_step(
        self,
        topic: str,
        num_steps: int = 5
    ) -> Dict[str, any]:
        """
        Create step-by-step explanation of a topic or process
        
        Args:
            topic: Topic or process to explain
            num_steps: Number of steps
            
        Returns:
            Dictionary with steps
        """
        try:
            logger.info(f"👣 Creating step-by-step explanation: {topic}")
            
            Validators.is_valid_topic(topic)
            
            system_prompt = f"""You are an expert educator. Break down '{topic}' into exactly {num_steps} clear steps.

For each step, provide:
- Step number and title
- Detailed explanation
- Key points to remember
- Common mistakes to avoid

Format as numbered list with clear sections."""
            
            user_prompt = f"Create a {num_steps}-step beginner-friendly explanation of '{topic}'."
            
            steps_text = self.client.generate_text(
                user_prompt,
                system_prompt=system_prompt,
                temperature=0.6
            )
            
            # Parse steps
            steps = self._parse_steps(steps_text)
            
            return {
                "topic": topic,
                "total_steps": num_steps,
                "steps": steps,
                "full_guide": steps_text
            }
            
        except Exception as e:
            logger.error(f"❌ Step-by-step explanation failed: {str(e)}")
            raise
    
    def _parse_steps(self, steps_text: str) -> List[Dict]:
        """
        Parse step-by-step guide into structured format
        
        Args:
            steps_text: Raw steps text
            
        Returns:
            List of structured steps
        """
        # Split by numbered bullets
        import re
        step_pattern = r'(?:^|\n)(?:\d+[.)\-]|\*)\s+(.+?)(?=\n\d+[.)\-]|\n\*|\Z)'
        matches = re.findall(step_pattern, steps_text, re.MULTILINE | re.DOTALL)
        
        return [{"step": i+1, "content": match.strip()} for i, match in enumerate(matches)]
