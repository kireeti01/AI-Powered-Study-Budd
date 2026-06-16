"""
Quiz Generator Module
Creates interactive quizzes with multiple question types
"""

import logging
import json
from typing import Dict, List, Optional
from pathlib import Path
from src.utils.gemini_client import get_gemini_client
from src.utils.pdf_processor import DocumentProcessor
from src.utils.validators import Validators
from src.config.settings import QUIZ_SETTINGS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuizGenerator:
    """
    Generates quizzes with various question types
    """
    
    QUESTION_TYPES = ["mcq", "true_false", "short_answer"]
    
    def __init__(self):
        """Initialize Quiz Generator"""
        self.client = get_gemini_client()
        logger.info("✅ Quiz Generator initialized")
    
    def generate_quiz(
        self,
        topic: str,
        num_questions: int = 10,
        question_types: List[str] = None,
        difficulty: str = "medium"
    ) -> Dict[str, any]:
        """
        Generate quiz on a topic
        
        Args:
            topic: Topic for quiz
            num_questions: Number of questions
            question_types: Types of questions (mcq, true_false, short_answer)
            difficulty: Question difficulty (easy, medium, hard)
            
        Returns:
            Dictionary with quiz questions
            
        Raises:
            ValueError: If parameters invalid
        """
        try:
            # Validate inputs
            Validators.is_valid_topic(topic)
            Validators.validate_quiz_params(num_questions, question_types or self.QUESTION_TYPES)
            
            question_types = question_types or self.QUESTION_TYPES
            
            logger.info(f"📋 Generating {num_questions} quiz questions on: {topic}")
            
            system_prompt = f"""You are an expert educator creating a quiz.
            
Requirements:
- Create {num_questions} questions about '{topic}'
- Difficulty level: {difficulty}
- Mix of question types: {', '.join(question_types)}
- Include clear answers and explanations
- Make questions test understanding, not memorization

Return response in JSON format with this structure:
{{
    "quiz_title": "string",
    "topic": "string",
    "difficulty": "string",
    "total_questions": number,
    "questions": [
        {{
            "id": number,
            "type": "mcq|true_false|short_answer",
            "question": "string",
            "options": ["string"] (for MCQ only),
            "correct_answer": "string",
            "explanation": "string"
        }}
    ]
}}"""
            
            user_prompt = f"""Generate a quiz with {num_questions} questions about '{topic}'.
            
Question distribution:
- MCQ: {num_questions // 2} questions
- True/False: {num_questions // 4} questions
- Short Answer: {num_questions // 4} questions

Make it {difficulty} level."""
            
            quiz_json = self.client.generate_structured_content(
                user_prompt,
                output_format="json",
                temperature=0.6
            )
            
            if not quiz_json or "questions" not in quiz_json:
                # Generate plain text alternative
                response = self.client.generate_text(user_prompt, system_prompt=system_prompt)
                quiz_json = {"quiz_title": f"Quiz: {topic}", "questions": response}
            
            logger.info(f"✅ Generated {num_questions} quiz questions")
            return quiz_json
            
        except Exception as e:
            logger.error(f"❌ Quiz generation failed: {str(e)}")
            raise
    
    def generate_quiz_from_notes(
        self,
        file_path: Path,
        num_questions: int = 10,
        question_types: List[str] = None,
        difficulty: str = "medium"
    ) -> Dict[str, any]:
        """
        Generate quiz from uploaded notes
        
        Args:
            file_path: Path to notes file
            num_questions: Number of questions
            question_types: Types of questions
            difficulty: Question difficulty
            
        Returns:
            Dictionary with quiz
        """
        try:
            logger.info(f"📄 Generating quiz from file: {file_path.name}")
            
            # Extract text from file
            text = DocumentProcessor.process_document(file_path, clean=True)
            
            # Generate quiz from text
            return self.generate_quiz_from_text(
                text,
                num_questions=num_questions,
                question_types=question_types,
                difficulty=difficulty
            )
            
        except Exception as e:
            logger.error(f"❌ Quiz generation from notes failed: {str(e)}")
            raise
    
    def generate_quiz_from_text(
        self,
        text: str,
        num_questions: int = 10,
        question_types: List[str] = None,
        difficulty: str = "medium"
    ) -> Dict[str, any]:
        """
        Generate quiz from provided text
        
        Args:
            text: Content for quiz
            num_questions: Number of questions
            question_types: Types of questions
            difficulty: Question difficulty
            
        Returns:
            Dictionary with quiz
        """
        try:
            Validators.is_non_empty_string(text)
            question_types = question_types or self.QUESTION_TYPES
            
            logger.info(f"📝 Generating {num_questions} questions from provided text")
            
            system_prompt = f"""You are an expert educator creating a quiz based on specific content.

Requirements:
- Create {num_questions} questions ONLY from the provided content
- Do NOT use external knowledge
- Difficulty: {difficulty}
- Include question types: {', '.join(question_types)}
- Each question must be answerable from the provided text
- Include clear answers and explanations

Return as JSON array with structure:
{{
    "questions": [
        {{
            "id": number,
            "type": "mcq|true_false|short_answer",
            "question": "string",
            "options": ["string"],
            "correct_answer": "string",
            "explanation": "string"
        }}
    ]
}}"""
            
            user_prompt = f"""Create a {num_questions}-question quiz based ONLY on this content:

CONTENT:
{text}

Create the quiz in JSON format."""
            
            quiz_data = self.client.generate_structured_content(
                user_prompt,
                output_format="json",
                temperature=0.6
            )
            
            if not isinstance(quiz_data, dict):
                quiz_data = {"questions": quiz_data}
            
            logger.info(f"✅ Generated quiz from text")
            return quiz_data
            
        except Exception as e:
            logger.error(f"❌ Quiz generation from text failed: {str(e)}")
            raise
    
    def evaluate_answer(
        self,
        question: str,
        user_answer: str,
        correct_answer: str,
        question_type: str = "short_answer"
    ) -> Dict[str, any]:
        """
        Evaluate user's answer to a question
        
        Args:
            question: The question asked
            user_answer: User's response
            correct_answer: Correct answer
            question_type: Type of question
            
        Returns:
            Dictionary with evaluation result
        """
        try:
            logger.info(f"✏️ Evaluating answer")
            
            system_prompt = """You are an expert grader. Evaluate student answers fairly.
            
For MCQ/True-False: Answer is correct or incorrect.
For Short Answer: Evaluate based on:
- Accuracy of information
- Completeness
- Clarity of explanation
- Key concepts mentioned

Return JSON with:
{
    "is_correct": boolean,
    "score": number (0-100),
    "feedback": "string",
    "explanation": "string"
}"""
            
            user_prompt = f"""Evaluate this answer:

Question: {question}
Question Type: {question_type}
Student's Answer: {user_answer}
Correct Answer: {correct_answer}

Provide evaluation in JSON format."""
            
            evaluation = self.client.generate_structured_content(
                user_prompt,
                output_format="json",
                temperature=0.5
            )
            
            logger.info(f"✅ Answer evaluated")
            return evaluation
            
        except Exception as e:
            logger.error(f"❌ Answer evaluation failed: {str(e)}")
            raise
    
    def generate_explanation(
        self,
        question: str,
        answer: str
    ) -> str:
        """
        Generate detailed explanation for an answer
        
        Args:
            question: The question
            answer: The answer to explain
            
        Returns:
            Detailed explanation
        """
        try:
            logger.info(f"💡 Generating explanation")
            
            system_prompt = """Provide a clear, detailed explanation that helps students understand.
            
Include:
- Why this answer is correct
- Key concepts involved
- Common misconceptions
- How to remember this
- Real-world applications"""
            
            user_prompt = f"""Explain why this is the correct answer:

Question: {question}
Answer: {answer}

Provide a detailed educational explanation."""
            
            explanation = self.client.generate_text(
                user_prompt,
                system_prompt=system_prompt,
                temperature=0.7
            )
            
            return explanation
            
        except Exception as e:
            logger.error(f"❌ Explanation generation failed: {str(e)}")
            raise
    
    def calculate_quiz_score(self, results: List[Dict]) -> Dict[str, any]:
        """
        Calculate quiz score from results
        
        Args:
            results: List of question results
            
        Returns:
            Dictionary with score details
        """
        try:
            total_questions = len(results)
            correct_count = sum(1 for r in results if r.get("is_correct", False))
            percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
            
            return {
                "total_questions": total_questions,
                "correct_answers": correct_count,
                "incorrect_answers": total_questions - correct_count,
                "percentage": round(percentage, 2),
                "score": correct_count,
                "grade": self._get_grade(percentage),
                "performance": self._get_performance_message(percentage)
            }
            
        except Exception as e:
            logger.error(f"❌ Score calculation failed: {str(e)}")
            raise
    
    @staticmethod
    def _get_grade(percentage: float) -> str:
        """Get letter grade from percentage"""
        if percentage >= 90:
            return "A"
        elif percentage >= 80:
            return "B"
        elif percentage >= 70:
            return "C"
        elif percentage >= 60:
            return "D"
        else:
            return "F"
    
    @staticmethod
    def _get_performance_message(percentage: float) -> str:
        """Get motivational performance message"""
        if percentage >= 90:
            return "🌟 Excellent! Outstanding performance!"
        elif percentage >= 80:
            return "✅ Great! Very good understanding!"
        elif percentage >= 70:
            return "👍 Good! Keep practicing to improve."
        elif percentage >= 60:
            return "📚 Okay! Review and try again."
        else:
            return "💪 Need more practice. Study the material again."
