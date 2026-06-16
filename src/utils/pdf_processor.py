"""
PDF Processing Utility
Extracts and processes text from PDF files
"""

import PyPDF2
import logging
from typing import Optional, List
from pathlib import Path
from src.config.settings import ERROR_MESSAGES, ALLOWED_FILE_TYPES, MAX_UPLOAD_SIZE_MB

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFProcessor:
    """
    Handle PDF file operations and text extraction
    """
    
    @staticmethod
    def validate_file(file_path: Path) -> bool:
        """
        Validate if file is allowed for processing
        
        Args:
            file_path: Path to file
            
        Returns:
            True if file is valid
            
        Raises:
            ValueError: If file is invalid
        """
        # Check file extension
        if file_path.suffix.lower() not in ALLOWED_FILE_TYPES:
            raise ValueError(ERROR_MESSAGES["invalid_file_type"])
        
        # Check file size
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        if file_size_mb > MAX_UPLOAD_SIZE_MB:
            raise ValueError(ERROR_MESSAGES["file_too_large"])
        
        return True
    
    @staticmethod
    def extract_text_from_pdf(file_path: Path) -> str:
        """
        Extract text from PDF file
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text from PDF
            
        Raises:
            ValueError: If text extraction fails
        """
        try:
            PDFProcessor.validate_file(file_path)
            
            text = ""
            
            with open(file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                num_pages = len(pdf_reader.pages)
                
                logger.info(f"📄 Processing PDF with {num_pages} pages")
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
                    
                if not text.strip():
                    raise ValueError(ERROR_MESSAGES["pdf_extraction_failed"])
                
                logger.info(f"✅ Successfully extracted {len(text)} characters from PDF")
                return text
                
        except ValueError as e:
            raise e
        except Exception as e:
            logger.error(f"❌ PDF extraction error: {str(e)}")
            raise ValueError(ERROR_MESSAGES["pdf_extraction_failed"])
    
    @staticmethod
    def extract_text_from_txt(file_path: Path) -> str:
        """
        Extract text from TXT file
        
        Args:
            file_path: Path to TXT file
            
        Returns:
            Text content
            
        Raises:
            ValueError: If reading fails
        """
        try:
            PDFProcessor.validate_file(file_path)
            
            with open(file_path, 'r', encoding='utf-8') as txt_file:
                text = txt_file.read()
            
            if not text.strip():
                raise ValueError(ERROR_MESSAGES["empty_content"])
            
            logger.info(f"✅ Successfully extracted {len(text)} characters from TXT file")
            return text
            
        except Exception as e:
            logger.error(f"❌ TXT extraction error: {str(e)}")
            raise ValueError(f"Failed to read text file: {str(e)}")
    
    @staticmethod
    def extract_text(file_path: Path) -> str:
        """
        Extract text from any supported file format
        
        Args:
            file_path: Path to file
            
        Returns:
            Extracted text
            
        Raises:
            ValueError: If extraction fails
        """
        file_path = Path(file_path)
        file_extension = file_path.suffix.lower()
        
        try:
            if file_extension == ".pdf":
                return PDFProcessor.extract_text_from_pdf(file_path)
            elif file_extension == ".txt":
                return PDFProcessor.extract_text_from_txt(file_path)
            else:
                raise ValueError(ERROR_MESSAGES["invalid_file_type"])
                
        except Exception as e:
            raise e
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """
        Split text into chunks for processing
        
        Args:
            text: Text to chunk
            chunk_size: Size of each chunk
            overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap
        
        logger.info(f"✅ Text split into {len(chunks)} chunks")
        return chunks
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize extracted text
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove special characters but keep basic punctuation
        text = ''.join(char if char.isalnum() or char.isspace() or char in '.,!?;:\'"-()\n' 
                      else '' for char in text)
        
        return text.strip()


class DocumentProcessor:
    """
    Higher-level document processing combining multiple utilities
    """
    
    @staticmethod
    def process_document(file_path: Path, clean: bool = True) -> str:
        """
        Process document and return cleaned text
        
        Args:
            file_path: Path to document
            clean: Whether to clean the text
            
        Returns:
            Processed text
        """
        try:
            text = PDFProcessor.extract_text(file_path)
            
            if clean:
                text = PDFProcessor.clean_text(text)
            
            return text
            
        except Exception as e:
            logger.error(f"❌ Document processing failed: {str(e)}")
            raise
    
    @staticmethod
    def process_and_chunk(file_path: Path, chunk_size: int = 1000) -> List[str]:
        """
        Process document and split into chunks
        
        Args:
            file_path: Path to document
            chunk_size: Size of chunks
            
        Returns:
            List of text chunks
        """
        try:
            text = PDFProcessor.process_document(file_path, clean=True)
            chunks = PDFProcessor.chunk_text(text, chunk_size=chunk_size)
            return chunks
            
        except Exception as e:
            logger.error(f"❌ Document chunking failed: {str(e)}")
            raise
