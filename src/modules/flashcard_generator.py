"""
Flashcard Generator Module
Creates and manages interactive flashcards
"""

import logging
import json
from typing import Dict, List, Optional
from pathlib import Path
from src.utils.gemini_client import get_gemini_client
from src.utils.pdf_processor import DocumentProcessor
from src.utils.text_processor import TextProcessor
from src.utils.validators import Validators
from src.config.settings import FLASHCARD_SETTINGS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FlashcardGenerator:
    """
    Generates and manages flashcards for efficient learning
    """
    
    def __init__(self):
        """Initialize Flashcard Generator"""
        self.client = get_gemini_client()
        logger.info("✅ Flashcard Generator initialized")
    
    def generate_flashcards(
        self,
        topic: str,
        num_cards: int = 15,
        card_type: str = "concept"
    ) -> Dict[str, any]:
        """
        Generate flashcards for a topic
        
        Args:
            topic: Topic for flashcards
            num_cards: Number of cards
            card_type: Type (concept, definition, question, scenario)
            
        Returns:
            Dictionary with flashcards
            
        Raises:
            ValueError: If parameters invalid
        """
        try:
            # Validate inputs
            Validators.is_valid_topic(topic)
            
            if num_cards < FLASHCARD_SETTINGS["min_cards"] or num_cards > FLASHCARD_SETTINGS["max_cards"]:
                raise ValueError(f"❌ Number of cards must be between {FLASHCARD_SETTINGS['min_cards']} and {FLASHCARD_SETTINGS['max_cards']}")
            
            logger.info(f"🃏 Generating {num_cards} flashcards on: {topic}")
            
            system_prompt = f"""You are an expert educator creating flashcards.
            
Requirements:
- Create {num_cards} flashcards about '{topic}'
- Type: {card_type} cards
- Front (question/prompt): concise, clear, focused
- Back (answer): comprehensive but brief
- Include memory aids or mnemonics where helpful
- Each card should be self-contained

Return as JSON array:
[
    {{
        "id": number,
        "front": "string",
        "back": "string",
        "difficulty": "easy|medium|hard",
        "memory_aid": "string or null"
    }}
]"""
            
            user_prompt = f"""Generate {num_cards} {card_type} flashcards about '{topic}'.

Make them:
- Focused and specific
- Easy to memorize
- Progressive in difficulty
- Varied in content"""
            
            cards = self.client.generate_structured_content(
                user_prompt,
                output_format="json",
                temperature=0.6
            )
            
            if isinstance(cards, dict) and "cards" in cards:
                cards = cards["cards"]
            elif not isinstance(cards, list):
                cards = [{"front": topic, "back": str(cards)}]
            
            logger.info(f"✅ Generated {len(cards)} flashcards")
            
            return {
                "topic": topic,
                "num_cards": len(cards),
                "card_type": card_type,
                "cards": cards
            }
            
        except Exception as e:
            logger.error(f"❌ Flashcard generation failed: {str(e)}")
            raise
    
    def generate_flashcards_from_notes(
        self,
        file_path: Path,
        num_cards: int = 15
    ) -> Dict[str, any]:
        """
        Generate flashcards from uploaded notes
        
        Args:
            file_path: Path to notes file
            num_cards: Number of cards
            
        Returns:
            Dictionary with flashcards
        """
        try:
            logger.info(f"📄 Generating flashcards from: {file_path.name}")
            
            # Extract text
            text = DocumentProcessor.process_document(file_path, clean=True)
            
            # Generate flashcards
            return self.generate_flashcards_from_text(
                text,
                num_cards=num_cards,
                title=file_path.stem
            )
            
        except Exception as e:
            logger.error(f"❌ Flashcard generation from notes failed: {str(e)}")
            raise
    
    def generate_flashcards_from_text(
        self,
        text: str,
        num_cards: int = 15,
        title: str = "Flashcards"
    ) -> Dict[str, any]:
        """
        Generate flashcards from provided text
        
        Args:
            text: Content for flashcards
            num_cards: Number of cards
            title: Flashcard deck title
            
        Returns:
            Dictionary with flashcards
        """
        try:
            Validators.is_non_empty_string(text)
            
            logger.info(f"📝 Generating {num_cards} flashcards from text")
            
            system_prompt = f"""Create {num_cards} flashcards based ONLY on the provided content.

Requirements:
- Each card has a front (question) and back (answer)
- Front: specific, focused prompt
- Back: clear, comprehensive answer
- All content from provided text ONLY
- Include difficulty rating
- Add memory tips where helpful

Format as JSON array:
[
    {{
        "id": number,
        "front": "string",
        "back": "string",
        "difficulty": "easy|medium|hard",
        "memory_aid": "string or null"
    }}
]"""
            
            user_prompt = f"""Create {num_cards} flashcards from this content:

CONTENT:
{text}

Return JSON array of flashcards."""
            
            cards = self.client.generate_structured_content(
                user_prompt,
                output_format="json",
                temperature=0.6
            )
            
            if isinstance(cards, dict) and "cards" in cards:
                cards = cards["cards"]
            elif not isinstance(cards, list):
                cards = []
            
            # Ensure we have the right number of cards
            cards = cards[:num_cards]
            
            return {
                "title": title,
                "num_cards": len(cards),
                "cards": cards
            }
            
        except Exception as e:
            logger.error(f"❌ Flashcard generation from text failed: {str(e)}")
            raise
    
    def export_to_anki(self, cards: List[Dict]) -> str:
        """
        Export flashcards to Anki format
        
        Args:
            cards: List of flashcard dictionaries
            
        Returns:
            Anki-formatted string
        """
        try:
            logger.info(f"💾 Exporting {len(cards)} cards to Anki format")
            
            # Anki format: front\tback\n
            anki_content = ""
            for card in cards:
                front = card.get("front", "").replace("\t", " ").replace("\n", " ")
                back = card.get("back", "").replace("\t", " ").replace("\n", " ")
                anki_content += f"{front}\t{back}\n"
            
            return anki_content
            
        except Exception as e:
            logger.error(f"❌ Anki export failed: {str(e)}")
            raise
    
    def export_to_csv(self, cards: List[Dict]) -> str:
        """
        Export flashcards to CSV format
        
        Args:
            cards: List of flashcard dictionaries
            
        Returns:
            CSV-formatted string
        """
        try:
            logger.info(f"💾 Exporting {len(cards)} cards to CSV format")
            
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow(["ID", "Front", "Back", "Difficulty", "Memory Aid"])
            
            # Write cards
            for card in cards:
                writer.writerow([
                    card.get("id", ""),
                    card.get("front", ""),
                    card.get("back", ""),
                    card.get("difficulty", ""),
                    card.get("memory_aid", "")
                ])
            
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"❌ CSV export failed: {str(e)}")
            raise
    
    def export_to_json(self, cards: List[Dict]) -> str:
        """
        Export flashcards to JSON format
        
        Args:
            cards: List of flashcard dictionaries
            
        Returns:
            JSON-formatted string
        """
        try:
            logger.info(f"💾 Exporting {len(cards)} cards to JSON format")
            
            return json.dumps(cards, indent=2)
            
        except Exception as e:
            logger.error(f"❌ JSON export failed: {str(e)}")
            raise
    
    def get_spaced_repetition_schedule(
        self,
        num_cards: int,
        study_days: int = 30
    ) -> Dict[str, any]:
        """
        Generate spaced repetition study schedule
        
        Args:
            num_cards: Number of cards in deck
            study_days: Study period in days
            
        Returns:
            Dictionary with study schedule
        """
        try:
            logger.info(f"📅 Creating spaced repetition schedule")
            
            # Spaced repetition intervals: 1, 3, 7, 14, 30 days
            schedule = {
                "day_1": {"cards_to_review": num_cards, "description": "Learn all cards"},
                "day_2": {"cards_to_review": num_cards, "description": "First review"},
                "day_4": {"cards_to_review": int(num_cards * 0.7), "description": "Second review"},
                "day_11": {"cards_to_review": int(num_cards * 0.5), "description": "Third review"},
                "day_25": {"cards_to_review": int(num_cards * 0.3), "description": "Fourth review"},
                "day_60": {"cards_to_review": int(num_cards * 0.1), "description": "Final review"}
            }
            
            return {
                "total_cards": num_cards,
                "study_period_days": study_days,
                "schedule": schedule,
                "note": "Review cards according to this spaced repetition schedule for optimal learning"
            }
            
        except Exception as e:
            logger.error(f"❌ Schedule generation failed: {str(e)}")
            raise
    
    def calculate_study_time(
        self,
        num_cards: int,
        time_per_card_seconds: float = 10
    ) -> Dict[str, any]:
        """
        Calculate study time needed
        
        Args:
            num_cards: Number of cards
            time_per_card_seconds: Average time per card
            
        Returns:
            Dictionary with time estimates
        """
        try:
            total_seconds = num_cards * time_per_card_seconds
            total_minutes = total_seconds / 60
            total_hours = total_minutes / 60
            
            # Estimate based on spaced repetition
            total_study_sessions = 6  # Based on schedule
            avg_session_time = total_minutes / total_study_sessions
            
            return {
                "total_cards": num_cards,
                "time_per_card": f"{time_per_card_seconds}s",
                "estimated_total_minutes": round(total_minutes, 1),
                "estimated_total_hours": round(total_hours, 2),
                "estimated_sessions": total_study_sessions,
                "average_session_minutes": round(avg_session_time, 1),
                "recommendation": f"Study {avg_session_time:.0f} minutes per day for best results"
            }
            
        except Exception as e:
            logger.error(f"❌ Study time calculation failed: {str(e)}")
            raise
