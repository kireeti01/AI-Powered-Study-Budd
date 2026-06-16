"""
Study Planner Module
Creates personalized study schedules and learning paths
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from src.utils.gemini_client import get_gemini_client
from src.utils.validators import Validators

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StudyPlanner:
    """
    Generates personalized study schedules and plans
    """
    
    def __init__(self):
        """Initialize Study Planner"""
        self.client = get_gemini_client()
        logger.info("✅ Study Planner initialized")
    
    def create_study_schedule(
        self,
        exam_date: str,
        topics: List[str],
        daily_hours: float,
        learning_style: str = "mixed"
    ) -> Dict[str, any]:
        """
        Create a personalized study schedule
        
        Args:
            exam_date: Exam date (YYYY-MM-DD)
            topics: List of topics to study
            daily_hours: Available study hours per day
            learning_style: Preferred learning style (visual, auditory, kinesthetic, mixed)
            
        Returns:
            Dictionary with study schedule
            
        Raises:
            ValueError: If parameters invalid
        """
        try:
            # Validate inputs
            Validators.is_valid_date(exam_date)
            Validators.validate_study_plan_params(exam_date, int(daily_hours))
            
            if not topics or not isinstance(topics, list):
                raise ValueError("❌ Provide at least one topic to study")
            
            logger.info(f"📚 Creating study schedule for {len(topics)} topics")
            
            # Calculate days until exam
            exam_dt = datetime.strptime(exam_date, "%Y-%m-%d")
            today = datetime.now()
            days_until_exam = (exam_dt - today).days
            
            # Generate schedule using AI
            system_prompt = """You are an expert academic advisor. Create a detailed, achievable study schedule.

Requirements:
- Break topics into manageable chunks
- Consider spaced repetition principles
- Include variety to maintain motivation
- Add breaks and review sessions
- Provide specific study techniques for each topic
- Include weekly milestones

Format as structured plan with daily tasks."""
            
            user_prompt = f"""Create a {days_until_exam}-day study schedule for exam on {exam_date}.

Topics to cover: {', '.join(topics)}
Available daily study time: {daily_hours} hours
Preferred learning style: {learning_style}

Provide day-by-day breakdown with:
1. Topics to focus on
2. Specific tasks
3. Study techniques
4. Review sessions
5. Practice tests"""
            
            schedule = self.client.generate_text(
                user_prompt,
                system_prompt=system_prompt,
                temperature=0.7
            )
            
            # Create structured schedule
            result = {
                "exam_date": exam_date,
                "days_until_exam": days_until_exam,
                "topics": topics,
                "daily_hours": daily_hours,
                "learning_style": learning_style,
                "total_study_hours": days_until_exam * daily_hours,
                "schedule": schedule,
                "start_date": today.strftime("%Y-%m-%d"),
                "milestones": self._create_milestones(topics, days_until_exam)
            }
            
            logger.info(f"✅ Created study schedule for {days_until_exam} days")
            return result
            
        except Exception as e:
            logger.error(f"❌ Study schedule creation failed: {str(e)}")
            raise
    
    def _create_milestones(self, topics: List[str], days: int) -> List[Dict]:
        """
        Create study milestones
        
        Args:
            topics: Topics to study
            days: Number of days available
            
        Returns:
            List of milestones
        """
        try:
            milestones = []
            interval = max(1, days // len(topics))
            
            for i, topic in enumerate(topics):
                day = (i + 1) * interval
                milestones.append({
                    "day": min(day, days),
                    "topic": topic,
                    "goal": f"Complete study of {topic}",
                    "deliverable": f"Create summary and flashcards for {topic}"
                })
            
            # Add final review milestone
            milestones.append({
                "day": days,
                "topic": "Final Review",
                "goal": "Review all topics",
                "deliverable": "Complete mock exam"
            })
            
            return milestones
            
        except Exception as e:
            logger.error(f"❌ Milestone creation failed: {str(e)}")
            return []
    
    def optimize_study_time(
        self,
        topics: List[str],
        available_hours: float,
        weak_areas: List[str] = None
    ) -> Dict[str, any]:
        """
        Optimize time allocation across topics
        
        Args:
            topics: List of topics
            available_hours: Total available study time
            weak_areas: Topics that need more focus
            
        Returns:
            Dictionary with optimized time allocation
        """
        try:
            logger.info(f"⏱️ Optimizing study time allocation")
            
            weak_areas = weak_areas or []
            
            # Calculate base allocation
            base_hours = available_hours / len(topics)
            allocation = {}
            remaining_hours = available_hours
            
            # Allocate more time to weak areas
            for topic in topics:
                if topic in weak_areas:
                    hours = base_hours * 1.5
                else:
                    hours = base_hours
                
                allocation[topic] = round(hours, 1)
                remaining_hours -= hours
            
            # Adjust for remaining hours
            if remaining_hours > 0:
                adjustment = remaining_hours / len(topics)
                for topic in allocation:
                    allocation[topic] += adjustment
            
            # Get AI recommendation
            system_prompt = """Analyze and optimize study time allocation.
            
Provide:
1. Recommended time per topic
2. Study intensity (light/medium/intense)
3. Best times to study each topic
4. Resource recommendations"""
            
            user_prompt = f"""Optimize this study time allocation:
            
Topics and allocated hours:
{json.dumps(allocation, indent=2)}

Weak areas needing focus: {', '.join(weak_areas) if weak_areas else 'None'}

Provide optimization recommendations."""
            
            recommendations = self.client.generate_text(
                user_prompt,
                system_prompt=system_prompt,
                temperature=0.7
            )
            
            return {
                "total_available_hours": available_hours,
                "time_allocation": allocation,
                "weak_areas": weak_areas,
                "recommendations": recommendations
            }
            
        except Exception as e:
            logger.error(f"❌ Study time optimization failed: {str(e)}")
            raise
    
    def create_weekly_plan(
        self,
        start_date: str,
        topics: List[str],
        daily_hours: float
    ) -> Dict[str, any]:
        """
        Create a weekly study plan
        
        Args:
            start_date: Week start date (YYYY-MM-DD)
            topics: Topics to cover this week
            daily_hours: Daily study time
            
        Returns:
            Dictionary with weekly plan
        """
        try:
            Validators.is_valid_date(start_date)
            
            logger.info(f"📖 Creating weekly study plan starting {start_date}")
            
            system_prompt = """Create a detailed weekly study plan.
            
Include:
1. Monday-Sunday breakdown
2. Specific topics per day
3. Study techniques
4. Practice problems
5. Review sessions
6. Milestone achievements"""
            
            topics_str = ", ".join(topics)
            user_prompt = f"""Create a weekly study plan starting {start_date}.
            
Topics to cover: {topics_str}
Daily study time available: {daily_hours} hours

Provide day-by-day detailed plan."""
            
            weekly_plan = self.client.generate_text(
                user_prompt,
                system_prompt=system_prompt,
                temperature=0.7
            )
            
            return {
                "week_start": start_date,
                "week_end": self._add_days(start_date, 6),
                "topics": topics,
                "daily_hours": daily_hours,
                "weekly_plan": weekly_plan,
                "total_weekly_hours": daily_hours * 7
            }
            
        except Exception as e:
            logger.error(f"❌ Weekly plan creation failed: {str(e)}")
            raise
    
    def suggest_study_techniques(
        self,
        topics: List[str],
        learning_style: str = "mixed"
    ) -> Dict[str, List[str]]:
        """
        Suggest study techniques for topics
        
        Args:
            topics: Topics to study
            learning_style: Student's learning style
            
        Returns:
            Dictionary with technique recommendations
        """
        try:
            logger.info(f"🎯 Suggesting study techniques")
            
            system_prompt = """Recommend effective study techniques for different learning styles.
            
Consider:
- Visual learners: diagrams, mind maps, flashcards
- Auditory learners: discussions, podcasts, explanations
- Kinesthetic learners: hands-on activities, practice problems
- Mixed learners: combination approaches"""
            
            topics_str = ", ".join(topics)
            user_prompt = f"""Suggest the best study techniques for a {learning_style} learner studying:
{topics_str}

For each topic, recommend:
1. Primary technique
2. Secondary technique
3. Practice method
4. Review method"""
            
            recommendations = self.client.generate_text(
                user_prompt,
                system_prompt=system_prompt,
                temperature=0.7
            )
            
            return {
                "learning_style": learning_style,
                "topics": topics,
                "recommendations": recommendations
            }
            
        except Exception as e:
            logger.error(f"❌ Technique suggestion failed: {str(e)}")
            raise
    
    def create_exam_readiness_checklist(
        self,
        topics: List[str],
        exam_date: str
    ) -> Dict[str, any]:
        """
        Create an exam readiness checklist
        
        Args:
            topics: Topics covered in exam
            exam_date: Exam date
            
        Returns:
            Dictionary with checklist
        """
        try:
            logger.info(f"✅ Creating exam readiness checklist")
            
            days_until_exam = (datetime.strptime(exam_date, "%Y-%m-%d") - datetime.now()).days
            
            system_prompt = """Create a comprehensive exam readiness checklist.
            
Include:
1. Topic mastery checklist
2. Practice test requirements
3. Day-before preparation
4. Exam day checklist
5. Materials to bring
6. Mental preparation tips"""
            
            topics_str = ", ".join(topics)
            user_prompt = f"""Create an exam readiness checklist for {days_until_exam} days away.
            
Topics: {topics_str}
Exam Date: {exam_date}

Provide a detailed, actionable checklist."""
            
            checklist = self.client.generate_text(
                user_prompt,
                system_prompt=system_prompt,
                temperature=0.7
            )
            
            return {
                "topics": topics,
                "exam_date": exam_date,
                "days_until_exam": days_until_exam,
                "checklist": checklist
            }
            
        except Exception as e:
            logger.error(f"❌ Checklist creation failed: {str(e)}")
            raise
    
    @staticmethod
    def _add_days(date_str: str, days: int) -> str:
        """Add days to a date string"""
        date = datetime.strptime(date_str, "%Y-%m-%d")
        new_date = date + timedelta(days=days)
        return new_date.strftime("%Y-%m-%d")


# Import json for study_planner module
import json
