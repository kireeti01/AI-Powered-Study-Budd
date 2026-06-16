"""
Configuration settings for AI Study Buddy Application
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
SRC_DIR = PROJECT_ROOT / "src"
TESTS_DIR = PROJECT_ROOT / "tests"
ASSETS_DIR = PROJECT_ROOT / "assets"
DOCS_DIR = PROJECT_ROOT / "docs"

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# File Upload Configuration
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE", "200"))
ALLOWED_FILE_TYPES = {".pdf", ".txt", ".docx"}
TEMP_DIR = Path(os.getenv("TEMP_DIR", "./temp"))

# Create temp directory if not exists
TEMP_DIR.mkdir(exist_ok=True)

# Cache Configuration
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "True").lower() == "true"
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # seconds

# Streamlit Configuration
STREAMLIT_CONFIG = {
    "page_title": "AI Study Buddy",
    "page_icon": "📚",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# AI Model Configuration
GEMINI_MODEL = "gemini-pro"
GEMINI_TEMPERATURE = 0.7
GEMINI_MAX_OUTPUT_TOKENS = 2000

# Quiz Configuration
QUIZ_SETTINGS = {
    "min_questions": 5,
    "max_questions": 20,
    "default_questions": 10,
    "question_types": ["mcq", "true_false", "short_answer"],
}

# Flashcard Configuration
FLASHCARD_SETTINGS = {
    "min_cards": 5,
    "max_cards": 50,
    "default_cards": 15,
}

# Study Planner Configuration
STUDY_PLANNER_SETTINGS = {
    "min_study_hours": 1,
    "max_study_hours": 8,
    "min_exam_days": 1,
    "max_exam_days": 365,
}

# Error Messages
ERROR_MESSAGES = {
    "api_key_missing": "❌ Gemini API key not found. Please add it to your .env file.",
    "file_too_large": f"❌ File size exceeds maximum limit of {MAX_UPLOAD_SIZE_MB}MB.",
    "invalid_file_type": "❌ Invalid file type. Supported: PDF, TXT, DOCX.",
    "api_error": "❌ API Error occurred. Please try again later.",
    "pdf_extraction_failed": "❌ Failed to extract text from PDF.",
    "empty_content": "❌ No content provided. Please enter text or upload a file.",
}

# Success Messages
SUCCESS_MESSAGES = {
    "api_connected": "✅ Successfully connected to Gemini API.",
    "content_processed": "✅ Content processed successfully.",
    "quiz_generated": "✅ Quiz generated successfully.",
    "flashcards_created": "✅ Flashcards created successfully.",
}

# Validation Settings
VALIDATION = {
    "min_topic_length": 3,
    "max_topic_length": 500,
    "min_question_length": 5,
    "max_question_length": 2000,
}

def validate_config():
    """Validate configuration settings"""
    if not GEMINI_API_KEY:
        raise ValueError(ERROR_MESSAGES["api_key_missing"])
    return True

# Configuration class for easy access
class Config:
    """Centralized configuration management"""
    
    API_KEY = GEMINI_API_KEY
    MODEL_NAME = GEMINI_MODEL
    TEMPERATURE = GEMINI_TEMPERATURE
    MAX_TOKENS = GEMINI_MAX_OUTPUT_TOKENS
    MAX_FILE_SIZE = MAX_UPLOAD_SIZE_MB
    DEBUG_MODE = DEBUG
    CACHE_ENABLED = CACHE_ENABLED
    CACHE_TTL = CACHE_TTL
