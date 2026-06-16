"""
Input Validation Utilities
Validates all user inputs
"""

import re
import logging
from typing import Optional
from src.config.settings import VALIDATION, ERROR_MESSAGES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Validators:
    """
    Collection of validation functions
    """
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Validate email format
        
        Args:
            email: Email address
            
        Returns:
            True if valid email
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def is_valid_topic(topic: str) -> bool:
        """
        Validate topic input
        
        Args:
            topic: Topic string
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If invalid
        """
        if not topic or not isinstance(topic, str):
            raise ValueError(ERROR_MESSAGES["empty_content"])
        
        topic = topic.strip()
        
        if len(topic) < VALIDATION["min_topic_length"]:
            raise ValueError(f"❌ Topic too short. Minimum {VALIDATION['min_topic_length']} characters required.")
        
        if len(topic) > VALIDATION["max_topic_length"]:
            raise ValueError(f"❌ Topic too long. Maximum {VALIDATION['max_topic_length']} characters allowed.")
        
        return True
    
    @staticmethod
    def is_valid_number(value: str, min_val: Optional[int] = None, 
                       max_val: Optional[int] = None) -> bool:
        """
        Validate numeric input
        
        Args:
            value: Value to validate
            min_val: Minimum value
            max_val: Maximum value
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If invalid
        """
        try:
            num = int(value)
            
            if min_val is not None and num < min_val:
                raise ValueError(f"❌ Value must be at least {min_val}")
            
            if max_val is not None and num > max_val:
                raise ValueError(f"❌ Value must be at most {max_val}")
            
            return True
            
        except ValueError as e:
            raise ValueError(f"❌ Invalid number: {str(e)}")
    
    @staticmethod
    def is_valid_date(date_str: str) -> bool:
        """
        Validate date format
        
        Args:
            date_str: Date string (YYYY-MM-DD)
            
        Returns:
            True if valid date
        """
        try:
            from datetime import datetime
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            raise ValueError("❌ Invalid date format. Use YYYY-MM-DD")
    
    @staticmethod
    def is_valid_file_size(size_bytes: int, max_size_mb: int) -> bool:
        """
        Validate file size
        
        Args:
            size_bytes: File size in bytes
            max_size_mb: Maximum allowed size in MB
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If file too large
        """
        max_bytes = max_size_mb * 1024 * 1024
        
        if size_bytes > max_bytes:
            raise ValueError(f"❌ File size exceeds {max_size_mb}MB limit")
        
        return True
    
    @staticmethod
    def is_non_empty_string(text: str) -> bool:
        """
        Check if string is non-empty
        
        Args:
            text: Text to check
            
        Returns:
            True if non-empty
            
        Raises:
            ValueError: If empty
        """
        if not text or not text.strip():
            raise ValueError(ERROR_MESSAGES["empty_content"])
        
        return True
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """
        Sanitize user input
        
        Args:
            text: Raw input
            
        Returns:
            Sanitized text
        """
        # Remove leading/trailing whitespace
        text = text.strip()
        
        # Remove extra spaces
        text = ' '.join(text.split())
        
        # Remove potentially harmful characters
        text = re.sub(r'[<>]', '', text)
        
        return text
    
    @staticmethod
    def validate_quiz_params(num_questions: int, question_types: list) -> bool:
        """
        Validate quiz generation parameters
        
        Args:
            num_questions: Number of questions
            question_types: List of question types
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If invalid
        """
        from src.config.settings import QUIZ_SETTINGS
        
        if num_questions < QUIZ_SETTINGS["min_questions"]:
            raise ValueError(f"❌ Minimum {QUIZ_SETTINGS['min_questions']} questions required")
        
        if num_questions > QUIZ_SETTINGS["max_questions"]:
            raise ValueError(f"❌ Maximum {QUIZ_SETTINGS['max_questions']} questions allowed")
        
        if not question_types:
            raise ValueError("❌ At least one question type must be selected")
        
        valid_types = set(QUIZ_SETTINGS["question_types"])
        for qtype in question_types:
            if qtype not in valid_types:
                raise ValueError(f"❌ Invalid question type: {qtype}")
        
        return True
    
    @staticmethod
    def validate_study_plan_params(exam_date: str, study_hours: int) -> bool:
        """
        Validate study plan parameters
        
        Args:
            exam_date: Exam date (YYYY-MM-DD)
            study_hours: Study hours per day
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If invalid
        """
        from src.config.settings import STUDY_PLANNER_SETTINGS
        from datetime import datetime
        
        # Validate date
        Validators.is_valid_date(exam_date)
        
        # Check if exam date is in future
        exam = datetime.strptime(exam_date, "%Y-%m-%d")
        today = datetime.now()
        days_left = (exam - today).days
        
        if days_left < STUDY_PLANNER_SETTINGS["min_exam_days"]:
            raise ValueError(f"❌ Exam should be at least {STUDY_PLANNER_SETTINGS['min_exam_days']} day away")
        
        if days_left > STUDY_PLANNER_SETTINGS["max_exam_days"]:
            raise ValueError(f"❌ Exam date cannot be more than {STUDY_PLANNER_SETTINGS['max_exam_days']} days away")
        
        # Validate study hours
        if study_hours < STUDY_PLANNER_SETTINGS["min_study_hours"]:
            raise ValueError(f"❌ Minimum {STUDY_PLANNER_SETTINGS['min_study_hours']} study hour required")
        
        if study_hours > STUDY_PLANNER_SETTINGS["max_study_hours"]:
            raise ValueError(f"❌ Maximum {STUDY_PLANNER_SETTINGS['max_study_hours']} study hours per day")
        
        return True
