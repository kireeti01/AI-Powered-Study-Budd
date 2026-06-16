"""
AI Study Buddy - Main Package
"""

__version__ = "1.0.0"
__author__ = "AI Study Buddy Team"
__description__ = "An AI-powered learning assistant for students"

from src.config.settings import Config, validate_config

__all__ = ["Config", "validate_config"]
