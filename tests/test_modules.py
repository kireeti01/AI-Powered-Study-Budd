"""
Unit Tests for AI Study Buddy Modules
Tests all backend and utility modules
"""

import unittest
import tempfile
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.text_processor import TextProcessor, QuestionProcessor
from src.utils.validators import Validators


class TestTextProcessor(unittest.TestCase):
    """Test TextProcessor utilities"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_text = """
        Photosynthesis is the process by which plants make their own food.
        It occurs in the chloroplasts of plant cells.
        The process converts light energy into chemical energy.
        """
    
    def test_clean_text(self):
        """Test text cleaning"""
        dirty_text = "  Hello   world!  This  is  messy.  "
        cleaned = TextProcessor.clean_text(dirty_text)
        self.assertEqual(cleaned, "Hello world! This is messy.")
    
    def test_split_into_sentences(self):
        """Test sentence splitting"""
        sentences = TextProcessor.split_into_sentences(self.sample_text)
        self.assertGreater(len(sentences), 0)
        self.assertTrue(all(isinstance(s, str) for s in sentences))
    
    def test_split_into_paragraphs(self):
        """Test paragraph splitting"""
        multi_para = "Para 1.\n\nPara 2.\n\nPara 3."
        paragraphs = TextProcessor.split_into_paragraphs(multi_para)
        self.assertEqual(len(paragraphs), 3)
    
    def test_count_words(self):
        """Test word counting"""
        count = TextProcessor.count_words(self.sample_text)
        self.assertGreater(count, 0)
    
    def test_get_text_statistics(self):
        """Test text statistics"""
        stats = TextProcessor.get_text_statistics(self.sample_text)
        self.assertIn("character_count", stats)
        self.assertIn("word_count", stats)
        self.assertIn("sentence_count", stats)
    
    def test_extract_urls(self):
        """Test URL extraction"""
        text_with_urls = "Visit https://example.com and http://test.org"
        urls = TextProcessor.extract_urls(text_with_urls)
        self.assertEqual(len(urls), 2)
    
    def test_remove_urls(self):
        """Test URL removal"""
        text = "Visit https://example.com today"
        cleaned = TextProcessor.remove_urls(text)
        self.assertNotIn("https", cleaned)


class TestQuestionProcessor(unittest.TestCase):
    """Test QuestionProcessor utilities"""
    
    def test_validate_question_valid(self):
        """Test valid question validation"""
        result = QuestionProcessor.validate_question("What is Python?")
        self.assertTrue(result)
    
    def test_validate_question_too_short(self):
        """Test short question rejection"""
        with self.assertRaises(ValueError):
            QuestionProcessor.validate_question("Hi")
    
    def test_format_question(self):
        """Test question formatting"""
        formatted = QuestionProcessor.format_question("what is this")
        self.assertTrue(formatted[0].isupper())
        self.assertTrue(formatted.endswith("?"))
    
    def test_extract_questions(self):
        """Test question extraction"""
        text = "What is photosynthesis? How does it work? Tell me about plants."
        questions = QuestionProcessor.extract_questions(text)
        self.assertEqual(len(questions), 2)


class TestValidators(unittest.TestCase):
    """Test Validators utilities"""
    
    def test_is_valid_email(self):
        """Test email validation"""
        self.assertTrue(Validators.is_valid_email("test@example.com"))
        self.assertFalse(Validators.is_valid_email("invalid-email"))
    
    def test_is_valid_topic(self):
        """Test topic validation"""
        result = Validators.is_valid_topic("Machine Learning")
        self.assertTrue(result)
    
    def test_is_valid_topic_too_short(self):
        """Test short topic rejection"""
        with self.assertRaises(ValueError):
            Validators.is_valid_topic("AI")
    
    def test_is_valid_number(self):
        """Test number validation"""
        result = Validators.is_valid_number("42", min_val=0, max_val=100)
        self.assertTrue(result)
    
    def test_is_valid_number_out_of_range(self):
        """Test number range validation"""
        with self.assertRaises(ValueError):
            Validators.is_valid_number("150", min_val=0, max_val=100)
    
    def test_is_valid_date(self):
        """Test date validation"""
        result = Validators.is_valid_date("2024-12-25")
        self.assertTrue(result)
    
    def test_is_valid_date_invalid(self):
        """Test invalid date rejection"""
        with self.assertRaises(ValueError):
            Validators.is_valid_date("25-12-2024")
    
    def test_sanitize_input(self):
        """Test input sanitization"""
        dirty = "  hello <script> world  "
        clean = Validators.sanitize_input(dirty)
        self.assertNotIn("<", clean)
        self.assertNotIn(">", clean)


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_text_pipeline(self):
        """Test text processing pipeline"""
        # Clean -> Count -> Analyze
        text = "  Hello!  This  is  a  test.  "
        cleaned = TextProcessor.clean_text(text)
        word_count = TextProcessor.count_words(cleaned)
        
        self.assertGreater(word_count, 0)
        self.assertEqual(cleaned.count("  "), 0)


class TestModuleImports(unittest.TestCase):
    """Test that all modules can be imported"""
    
    def test_import_gemini_client(self):
        """Test GeminiClient import"""
        try:
            from src.utils.gemini_client import GeminiClient, get_gemini_client
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import GeminiClient: {str(e)}")
    
    def test_import_pdf_processor(self):
        """Test PDFProcessor import"""
        try:
            from src.utils.pdf_processor import PDFProcessor, DocumentProcessor
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import PDFProcessor: {str(e)}")
    
    def test_import_modules(self):
        """Test all module imports"""
        try:
            from src.modules.topic_explainer import TopicExplainer
            from src.modules.notes_summarizer import NotesSummarizer
            from src.modules.quiz_generator import QuizGenerator
            from src.modules.flashcard_generator import FlashcardGenerator
            from src.modules.study_planner import StudyPlanner
            from src.modules.qa_engine import QAEngine
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import modules: {str(e)}")


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests
    suite.addTests(loader.loadTestsFromTestCase(TestTextProcessor))
    suite.addTests(loader.loadTestsFromTestCase(TestQuestionProcessor))
    suite.addTests(loader.loadTestsFromTestCase(TestValidators))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestModuleImports))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
