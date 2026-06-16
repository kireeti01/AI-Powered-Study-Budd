"""
Q&A Engine Module
Answers questions based on uploaded study materials
"""

import logging
from typing import Dict, List, Optional
from pathlib import Path
from src.utils.gemini_client import get_gemini_client
from src.utils.pdf_processor import DocumentProcessor
from src.utils.text_processor import TextProcessor, QuestionProcessor
from src.utils.validators import Validators

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QAEngine:
    """
    Question-Answering engine that answers questions based on provided context
    """
    
    def __init__(self):
        """Initialize QA Engine"""
        self.client = get_gemini_client()
        self.context = ""
        logger.info("✅ QA Engine initialized")
    
    def load_context_from_file(self, file_path: Path) -> bool:
        """
        Load context from a file
        
        Args:
            file_path: Path to file
            
        Returns:
            True if loaded successfully
            
        Raises:
            Exception: If file loading fails
        """
        try:
            logger.info(f"📄 Loading context from: {file_path.name}")
            
            self.context = DocumentProcessor.process_document(file_path, clean=True)
            
            logger.info(f"✅ Loaded {len(self.context)} characters from file")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load context: {str(e)}")
            raise
    
    def load_context_from_text(self, text: str) -> bool:
        """
        Load context from text
        
        Args:
            text: Context text
            
        Returns:
            True if loaded successfully
            
        Raises:
            ValueError: If text is invalid
        """
        try:
            Validators.is_non_empty_string(text)
            
            logger.info(f"📝 Loading context from text")
            
            self.context = TextProcessor.clean_text(text)
            
            logger.info(f"✅ Loaded {len(self.context)} characters")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load context: {str(e)}")
            raise
    
    def answer_question(
        self,
        question: str,
        answer_length: str = "medium"
    ) -> Dict[str, str]:
        """
        Answer a question based on loaded context
        
        Args:
            question: Question to answer
            answer_length: Length of answer (short, medium, long)
            
        Returns:
            Dictionary with question and answer
            
        Raises:
            ValueError: If no context loaded or question invalid
        """
        try:
            if not self.context:
                raise ValueError("❌ No study material loaded. Please upload a file or enter text first.")
            
            # Validate question
            QuestionProcessor.validate_question(question)
            question = QuestionProcessor.format_question(question)
            
            logger.info(f"❓ Answering question: {question}")
            
            length_instructions = {
                "short": "in 2-3 sentences",
                "medium": "in 3-5 sentences",
                "long": "in 1-2 paragraphs"
            }
            
            length_instruction = length_instructions.get(answer_length, "in detail")
            
            system_prompt = """You are a helpful tutor. Answer questions ONLY based on the provided context.
            
Rules:
1. Answer ONLY using information from the context
2. If the context doesn't contain the answer, say so clearly
3. Be accurate and cite relevant parts of the material
4. Provide clear, educational explanations
5. Include examples when helpful"""
            
            user_prompt = f"""Based on the following study material, answer this question {length_instruction}:

CONTEXT:
{self.context}

QUESTION: {question}

ANSWER:"""
            
            answer = self.client.generate_text(
                user_prompt,
                system_prompt=system_prompt,
                temperature=0.5
            )
            
            logger.info(f"✅ Question answered successfully")
            
            return {
                "question": question,
                "answer": answer,
                "answer_length": answer_length,
                "context_used": len(self.context) > 0
            }
            
        except Exception as e:
            logger.error(f"❌ Question answering failed: {str(e)}")
            raise
    
    def ask_multiple_questions(
        self,
        questions: List[str]
    ) -> List[Dict[str, str]]:
        """
        Answer multiple questions
        
        Args:
            questions: List of questions
            
        Returns:
            List of question-answer pairs
        """
        try:
            if not self.context:
                raise ValueError("❌ No study material loaded.")
            
            logger.info(f"❓ Answering {len(questions)} questions")
            
            answers = []
            for question in questions:
                try:
                    result = self.answer_question(question)
                    answers.append(result)
                except Exception as e:
                    logger.warning(f"⚠️ Failed to answer question: {question}")
                    answers.append({
                        "question": question,
                        "answer": f"Error answering question: {str(e)}",
                        "error": True
                    })
            
            logger.info(f"✅ Answered {len(answers)} questions")
            return answers
            
        except Exception as e:
            logger.error(f"❌ Batch question answering failed: {str(e)}")
            raise
    
    def generate_follow_up_questions(
        self,
        question: str,
        num_questions: int = 3
    ) -> List[str]:
        """
        Generate follow-up questions based on a question
        
        Args:
            question: Original question
            num_questions: Number of follow-ups to generate
            
        Returns:
            List of follow-up questions
        """
        try:
            logger.info(f"🔗 Generating {num_questions} follow-up questions")
            
            system_prompt = f"""Generate {num_questions} natural follow-up questions that help deepen understanding.
            
Requirements:
- Logical progression
- Build on the original question
- Test deeper understanding
- Vary in approach (why, how, when, etc.)
- Progressively more challenging"""
            
            user_prompt = f"""Based on this question, generate {num_questions} follow-up questions:

Original Question: {question}

Generate follow-up questions as a numbered list."""
            
            response = self.client.generate_text(
                user_prompt,
                system_prompt=system_prompt,
                temperature=0.7
            )
            
            # Parse follow-up questions
            follow_ups = self._parse_follow_up_questions(response)
            
            logger.info(f"✅ Generated {len(follow_ups)} follow-up questions")
            return follow_ups
            
        except Exception as e:
            logger.error(f"❌ Follow-up question generation failed: {str(e)}")
            raise
    
    def _parse_follow_up_questions(self, response: str) -> List[str]:
        """
        Parse follow-up questions from response
        
        Args:
            response: Raw response text
            
        Returns:
            List of parsed questions
        """
        import re
        
        # Extract numbered questions
        pattern = r'^\d+\.\s*(.+?)$'
        matches = re.findall(pattern, response, re.MULTILINE)
        
        questions = [q.strip() for q in matches if q.strip()]
        
        return questions
    
    def verify_answer(
        self,
        question: str,
        given_answer: str
    ) -> Dict[str, any]:
        """
        Verify if an answer is correct based on context
        
        Args:
            question: The question
            given_answer: Student's answer
            
        Returns:
            Dictionary with verification result
        """
        try:
            if not self.context:
                raise ValueError("❌ No study material loaded.")
            
            logger.info(f"✅ Verifying answer to question: {question}")
            
            system_prompt = """You are an expert grader. Evaluate answers based ONLY on the provided context.
            
Provide:
1. Is the answer correct? (yes/no/partially)
2. Score (0-100)
3. What's correct or missing
4. Correct answer if needed
5. Explanation"""
            
            user_prompt = f"""Based on this context, evaluate the student's answer.

CONTEXT:
{self.context}

QUESTION: {question}
STUDENT'S ANSWER: {given_answer}

Evaluate and provide feedback in detail."""
            
            evaluation = self.client.generate_text(
                user_prompt,
                system_prompt=system_prompt,
                temperature=0.5
            )
            
            return {
                "question": question,
                "given_answer": given_answer,
                "evaluation": evaluation,
                "verified_against_context": True
            }
            
        except Exception as e:
            logger.error(f"❌ Answer verification failed: {str(e)}")
            raise
    
    def search_context(self, search_query: str) -> List[str]:
        """
        Search for relevant information in context
        
        Args:
            search_query: Search query
            
        Returns:
            List of relevant passages
        """
        try:
            if not self.context:
                raise ValueError("❌ No study material loaded.")
            
            logger.info(f"🔍 Searching for: {search_query}")
            
            # Split context into sentences
            sentences = TextProcessor.split_into_sentences(self.context)
            
            # Simple keyword search (could be enhanced with embedding-based search)
            query_words = search_query.lower().split()
            relevant_sentences = []
            
            for sentence in sentences:
                sentence_lower = sentence.lower()
                if any(word in sentence_lower for word in query_words):
                    relevant_sentences.append(sentence)
            
            logger.info(f"✅ Found {len(relevant_sentences)} relevant passages")
            return relevant_sentences
            
        except Exception as e:
            logger.error(f"❌ Context search failed: {str(e)}")
            raise
    
    def get_context_summary(self) -> Dict[str, any]:
        """
        Get summary statistics of loaded context
        
        Returns:
            Dictionary with context statistics
        """
        try:
            if not self.context:
                raise ValueError("❌ No study material loaded.")
            
            logger.info(f"📊 Generating context summary")
            
            stats = TextProcessor.get_text_statistics(self.context)
            
            return {
                "context_loaded": True,
                "statistics": stats,
                "can_answer_questions": True
            }
            
        except Exception as e:
            logger.error(f"❌ Summary generation failed: {str(e)}")
            raise
    
    def clear_context(self) -> bool:
        """
        Clear loaded context
        
        Returns:
            True if cleared successfully
        """
        try:
            self.context = ""
            logger.info(f"🗑️ Context cleared")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to clear context: {str(e)}")
            return False
