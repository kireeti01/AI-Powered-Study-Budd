"""
Notes Summarizer Module
Summarizes uploaded documents and extracts key information
"""

import logging
from typing import Dict, List, Optional
from pathlib import Path
from src.utils.gemini_client import get_gemini_client
from src.utils.pdf_processor import PDFProcessor, DocumentProcessor
from src.utils.text_processor import TextProcessor
from src.utils.validators import Validators

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotesSummarizer:
    """
    Summarizes notes and documents using AI
    """
    
    SUMMARY_LENGTHS = {
        "short": 100,
        "medium": 300,
        "long": 500
    }
    
    def __init__(self):
        """Initialize Notes Summarizer"""
        self.client = get_gemini_client()
        logger.info("✅ Notes Summarizer initialized")
    
    def summarize_text(
        self,
        text: str,
        length: str = "medium",
        include_keypoints: bool = True,
        include_keywords: bool = True
    ) -> Dict[str, any]:
        """
        Summarize provided text
        
        Args:
            text: Text to summarize
            length: Summary length (short, medium, long)
            include_keypoints: Include key points
            include_keywords: Include important keywords
            
        Returns:
            Dictionary with summary and analysis
            
        Raises:
            ValueError: If text is invalid
        """
        try:
            # Validate input
            Validators.is_non_empty_string(text)
            
            if length not in self.SUMMARY_LENGTHS:
                raise ValueError(f"❌ Invalid length. Choose from: {list(self.SUMMARY_LENGTHS.keys())}")
            
            target_words = self.SUMMARY_LENGTHS[length]
            logger.info(f"📝 Summarizing {len(text)} characters to {length} summary")
            
            # Build prompt
            system_prompt = """You are an expert note-taker. Create concise, informative summaries.
            
Key requirements:
- Focus on the most important information
- Use clear, simple language
- Maintain the original meaning
- Organize logically
- Include all critical concepts"""
            
            user_prompt = f"""Please summarize the following text in approximately {target_words} words.
Aim for clarity and completeness.

TEXT:
{text}

SUMMARY:"""
            
            summary = self.client.generate_text(
                user_prompt,
                system_prompt=system_prompt,
                temperature=0.5
            )
            
            # Extract analysis
            result = {
                "original_length": len(text),
                "summary_length": len(summary),
                "compression_ratio": len(summary) / len(text),
                "summary": summary
            }
            
            if include_keypoints:
                result["key_points"] = self._extract_key_points(text, summary)
            
            if include_keywords:
                result["keywords"] = TextProcessor.extract_key_phrases(text, num_phrases=10)
            
            logger.info(f"✅ Successfully summarized text")
            return result
            
        except Exception as e:
            logger.error(f"❌ Text summarization failed: {str(e)}")
            raise
    
    def summarize_file(
        self,
        file_path: Path,
        length: str = "medium",
        include_keypoints: bool = True
    ) -> Dict[str, any]:
        """
        Summarize uploaded file (PDF or TXT)
        
        Args:
            file_path: Path to file
            length: Summary length
            include_keypoints: Include key points
            
        Returns:
            Dictionary with file summary
        """
        try:
            logger.info(f"📄 Processing file: {file_path}")
            
            # Process document
            text = DocumentProcessor.process_document(file_path, clean=True)
            
            # Summarize
            result = self.summarize_text(
                text,
                length=length,
                include_keypoints=include_keypoints,
                include_keywords=True
            )
            
            result["filename"] = file_path.name
            result["file_size"] = file_path.stat().st_size
            
            logger.info(f"✅ Successfully summarized file: {file_path.name}")
            return result
            
        except Exception as e:
            logger.error(f"❌ File summarization failed: {str(e)}")
            raise
    
    def _extract_key_points(self, original_text: str, summary: str) -> List[str]:
        """
        Extract key points from text and summary
        
        Args:
            original_text: Original content
            summary: Summary text
            
        Returns:
            List of key points
        """
        try:
            # Use summary to extract key points
            sentences = TextProcessor.split_into_sentences(summary)
            
            # Return as key points
            key_points = [s for s in sentences if len(s) > 10][:5]
            
            return key_points
            
        except Exception as e:
            logger.error(f"❌ Key point extraction failed: {str(e)}")
            return []
    
    def create_outline(
        self,
        text: str,
        max_levels: int = 3
    ) -> Dict[str, any]:
        """
        Create hierarchical outline of document
        
        Args:
            text: Document text
            max_levels: Maximum outline levels
            
        Returns:
            Dictionary with outline structure
        """
        try:
            logger.info(f"🗂️ Creating outline from text")
            
            Validators.is_non_empty_string(text)
            
            system_prompt = f"""Create a structured outline of the provided text.
            
Requirements:
- Use up to {max_levels} levels of hierarchy
- Use bullet points for hierarchy
- Keep topics concise (3-10 words each)
- Include all major sections and subsections
- Make it easy to scan"""
            
            user_prompt = f"""Create a detailed outline of this text:

{text}

Format as a hierarchical outline."""
            
            outline = self.client.generate_text(
                user_prompt,
                system_prompt=system_prompt,
                temperature=0.5
            )
            
            return {
                "original_length": len(text),
                "outline": outline,
                "max_levels": max_levels
            }
            
        except Exception as e:
            logger.error(f"❌ Outline creation failed: {str(e)}")
            raise
    
    def extract_definitions(self, text: str, num_definitions: int = 10) -> List[Dict]:
        """
        Extract and define key terms from text
        
        Args:
            text: Document text
            num_definitions: Number of definitions to extract
            
        Returns:
            List of term-definition pairs
        """
        try:
            logger.info(f"📖 Extracting {num_definitions} key terms")
            
            system_prompt = """Extract important technical terms and provide simple definitions.
            
For each term:
- Term name
- Simple definition (1-2 sentences)
- Context of use"""
            
            user_prompt = f"""Extract the {num_definitions} most important terms from this text and define them simply:

{text}

Format as a numbered list with: Term | Definition"""
            
            response = self.client.generate_text(
                user_prompt,
                system_prompt=system_prompt,
                temperature=0.6
            )
            
            # Parse definitions
            definitions = self._parse_definitions(response)
            
            logger.info(f"✅ Extracted {len(definitions)} definitions")
            return definitions
            
        except Exception as e:
            logger.error(f"❌ Definition extraction failed: {str(e)}")
            raise
    
    def _parse_definitions(self, response: str) -> List[Dict]:
        """
        Parse definitions from response
        
        Args:
            response: Raw response text
            
        Returns:
            List of parsed definitions
        """
        import re
        definitions = []
        
        # Split by numbered items
        items = re.split(r'\n\d+\.\s+', response)
        
        for item in items[1:]:  # Skip first empty item
            parts = item.split('|', 1)
            if len(parts) == 2:
                definitions.append({
                    "term": parts[0].strip(),
                    "definition": parts[1].strip()
                })
        
        return definitions
    
    def highlight_important_sections(
        self,
        text: str,
        num_sections: int = 5
    ) -> Dict[str, any]:
        """
        Identify and highlight most important sections
        
        Args:
            text: Document text
            num_sections: Number of important sections
            
        Returns:
            Dictionary with highlighted sections
        """
        try:
            logger.info(f"⭐ Highlighting {num_sections} important sections")
            
            system_prompt = f"""Identify the {num_sections} most important sections in the provided text.

For each section:
- Section name/title
- Why it's important
- Key content (2-3 sentences)"""
            
            user_prompt = f"""Identify and explain the {num_sections} most important sections:

{text}"""
            
            highlights = self.client.generate_text(
                user_prompt,
                system_prompt=system_prompt,
                temperature=0.6
            )
            
            return {
                "text_length": len(text),
                "num_sections": num_sections,
                "highlighted_sections": highlights
            }
            
        except Exception as e:
            logger.error(f"❌ Section highlighting failed: {str(e)}")
            raise
