"""
Text Processing Utilities
Handles text manipulation, validation, and processing
"""

import re
import logging
from typing import List, Tuple, Optional
from src.config.settings import VALIDATION, ERROR_MESSAGES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextProcessor:
    """
    Utility class for text processing operations
    """
    
    @staticmethod
    def validate_input(text: str, min_length: int = None, max_length: int = None) -> bool:
        """
        Validate text input
        
        Args:
            text: Text to validate
            min_length: Minimum length requirement
            max_length: Maximum length requirement
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If validation fails
        """
        if not text or not isinstance(text, str):
            raise ValueError(ERROR_MESSAGES["empty_content"])
        
        text = text.strip()
        text_length = len(text)
        
        min_len = min_length or VALIDATION["min_topic_length"]
        max_len = max_length or VALIDATION["max_topic_length"]
        
        if text_length < min_len:
            raise ValueError(f"❌ Input too short. Minimum {min_len} characters required.")
        
        if text_length > max_len:
            raise ValueError(f"❌ Input too long. Maximum {max_len} characters allowed.")
        
        return True
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove special characters except basic punctuation
        text = re.sub(r'[^\w\s.,!?;:\'"()\-\n]', '', text)
        
        return text.strip()
    
    @staticmethod
    def extract_key_phrases(text: str, num_phrases: int = 5) -> List[str]:
        """
        Extract key phrases from text
        
        Args:
            text: Input text
            num_phrases: Number of phrases to extract
            
        Returns:
            List of key phrases
        """
        # Simple implementation: split by punctuation and get longest phrases
        sentences = re.split(r'[.!?]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Sort by length and get top phrases
        key_phrases = sorted(sentences, key=len, reverse=True)[:num_phrases]
        
        logger.info(f"✅ Extracted {len(key_phrases)} key phrases")
        return key_phrases
    
    @staticmethod
    def summarize_text(text: str, num_sentences: int = 3) -> str:
        """
        Create a simple summary by extracting key sentences
        
        Args:
            text: Input text
            num_sentences: Number of sentences in summary
            
        Returns:
            Summarized text
        """
        try:
            sentences = re.split(r'[.!?]', text)
            sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
            
            # Get sentences with important keywords
            summary_sentences = sentences[:min(num_sentences, len(sentences))]
            summary = '. '.join(summary_sentences)
            
            if not summary.endswith('.'):
                summary += '.'
            
            logger.info(f"✅ Created summary with {num_sentences} sentences")
            return summary
            
        except Exception as e:
            logger.error(f"❌ Summarization failed: {str(e)}")
            return text[:500] + "..."
    
    @staticmethod
    def split_into_sentences(text: str) -> List[str]:
        """
        Split text into sentences
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        sentences = re.split(r'[.!?]\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        logger.info(f"✅ Split text into {len(sentences)} sentences")
        return sentences
    
    @staticmethod
    def split_into_paragraphs(text: str) -> List[str]:
        """
        Split text into paragraphs
        
        Args:
            text: Input text
            
        Returns:
            List of paragraphs
        """
        paragraphs = text.split('\n\n')
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        logger.info(f"✅ Split text into {len(paragraphs)} paragraphs")
        return paragraphs
    
    @staticmethod
    def count_words(text: str) -> int:
        """
        Count words in text
        
        Args:
            text: Input text
            
        Returns:
            Word count
        """
        return len(text.split())
    
    @staticmethod
    def get_text_statistics(text: str) -> dict:
        """
        Get comprehensive text statistics
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with statistics
        """
        sentences = TextProcessor.split_into_sentences(text)
        paragraphs = TextProcessor.split_into_paragraphs(text)
        words = text.split()
        
        stats = {
            "character_count": len(text),
            "word_count": len(words),
            "sentence_count": len(sentences),
            "paragraph_count": len(paragraphs),
            "average_word_length": sum(len(w) for w in words) / len(words) if words else 0,
            "average_sentence_length": len(words) / len(sentences) if sentences else 0,
        }
        
        logger.info(f"✅ Generated text statistics")
        return stats
    
    @staticmethod
    def format_as_markdown(text: str, bold_keywords: List[str] = None) -> str:
        """
        Format text as markdown with highlighting
        
        Args:
            text: Input text
            bold_keywords: Keywords to bold
            
        Returns:
            Markdown formatted text
        """
        formatted_text = text
        
        if bold_keywords:
            for keyword in bold_keywords:
                # Case-insensitive replacement
                pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                formatted_text = pattern.sub(f"**{keyword}**", formatted_text)
        
        return formatted_text
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """
        Extract URLs from text
        
        Args:
            text: Input text
            
        Returns:
            List of URLs
        """
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, text)
        
        logger.info(f"✅ Extracted {len(urls)} URLs")
        return urls
    
    @staticmethod
    def remove_urls(text: str) -> str:
        """
        Remove URLs from text
        
        Args:
            text: Input text
            
        Returns:
            Text without URLs
        """
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        cleaned_text = re.sub(url_pattern, '', text)
        
        return cleaned_text


class QuestionProcessor:
    """
    Utility class for processing questions
    """
    
    @staticmethod
    def validate_question(question: str) -> bool:
        """
        Validate if text is a valid question
        
        Args:
            question: Question text
            
        Returns:
            True if valid question
            
        Raises:
            ValueError: If not a valid question
        """
        question = question.strip()
        
        if not question:
            raise ValueError(ERROR_MESSAGES["empty_content"])
        
        if len(question) < VALIDATION["min_question_length"]:
            raise ValueError("❌ Question too short. Minimum 5 characters required.")
        
        if len(question) > VALIDATION["max_question_length"]:
            raise ValueError("❌ Question too long. Maximum 2000 characters allowed.")
        
        # Check if ends with question mark (optional but preferred)
        if not question.endswith('?') and not question.endswith('.'):
            question += '?'
        
        return True
    
    @staticmethod
    def extract_questions(text: str) -> List[str]:
        """
        Extract all questions from text
        
        Args:
            text: Input text
            
        Returns:
            List of questions
        """
        # Match text ending with ?
        questions = re.findall(r'[^.!?]*\?', text)
        questions = [q.strip() for q in questions if q.strip()]
        
        logger.info(f"✅ Extracted {len(questions)} questions from text")
        return questions
    
    @staticmethod
    def format_question(question: str) -> str:
        """
        Format and clean question text
        
        Args:
            question: Raw question
            
        Returns:
            Formatted question
        """
        question = question.strip()
        
        # Ensure starts with capital letter
        if question and question[0].islower():
            question = question[0].upper() + question[1:]
        
        # Ensure ends with ?
        if not question.endswith('?'):
            question += '?'
        
        return question
