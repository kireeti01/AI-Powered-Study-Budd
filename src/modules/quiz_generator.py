"""
Quiz Generator Module
Creates interactive quizzes with multiple question types
"""

import logging
import json
from typing import Dict, List
from pathlib import Path

from src.utils.gemini_client import get_gemini_client
from src.utils.pdf_processor import DocumentProcessor
from src.utils.validators import Validators


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuizGenerator:

    QUESTION_TYPES = [
        "mcq",
        "true_false",
        "short_answer"
    ]


    def __init__(self):

        self.client = get_gemini_client()

        logger.info("✅ Quiz Generator initialized")



    def _convert_to_dict(self, response):

        """
        Safely convert Gemini response to dictionary
        """

        if isinstance(response, dict):
            return response


        if isinstance(response, str):

            try:
                return json.loads(response)

            except:

                return {

                    "quiz_title":
                        "Generated Quiz",

                    "questions":[

                        {
                            "id":1,
                            "type":"short_answer",
                            "question":response,
                            "options":[],
                            "correct_answer":"",
                            "explanation":""
                        }

                    ]

                }


        return {

            "questions":[]

        }





    def generate_quiz(
            self,
            topic:str,
            num_questions:int=10,
            question_types=None,
            difficulty="medium"
    ):


        try:


            Validators.is_valid_topic(topic)


            prompt=f"""

You are an expert teacher.

Create a quiz about:

{topic}


Difficulty:
{difficulty}


Number of questions:
{num_questions}


Return ONLY JSON.


Format:

{{

"quiz_title":"",

"topic":"",

"difficulty":"",

"questions":[

{{

"id":1,

"type":"mcq",

"question":"",

"options":[

"",

"",

"",

""

],

"correct_answer":"",

"explanation":""

}}

]

}}

"""


            response=self.client.generate_structured_content(

                prompt,

                output_format="json",

                temperature=0.6

            )


            quiz=self._convert_to_dict(response)


            logger.info("✅ Quiz generated")


            return quiz



        except Exception as e:


            logger.error(
                f"Quiz generation failed: {e}"
            )

            raise





    def generate_quiz_from_text(
            self,
            text:str,
            num_questions=10,
            question_types=None,
            difficulty="medium"
    ):


        try:


            Validators.is_non_empty_string(text)



            prompt=f"""

Create quiz only from this content:


{text}



Create {num_questions} questions.


Return JSON:


{{

"questions":[

{{

"id":1,

"type":"mcq",

"question":"",

"options":[],

"correct_answer":"",

"explanation":""

}}

]

}}

"""


            response=self.client.generate_structured_content(

                prompt,

                output_format="json",

                temperature=0.6

            )



            return self._convert_to_dict(response)



        except Exception as e:


            logger.error(
                f"Quiz text generation failed: {e}"
            )

            raise






    def generate_quiz_from_notes(
            self,
            file_path:Path,
            num_questions=10,
            question_types=None,
            difficulty="medium"
    ):


        text=DocumentProcessor.process_document(

            file_path,

            clean=True

        )


        return self.generate_quiz_from_text(

            text,

            num_questions,

            question_types,

            difficulty

        )







    def evaluate_answer(
            self,
            question,
            user_answer,
            correct_answer,
            question_type="short_answer"

    ):


        prompt=f"""

Evaluate answer:


Question:
{question}


Student answer:
{user_answer}


Correct answer:
{correct_answer}


Return JSON:


{{

"is_correct":true,

"score":100,

"feedback":"",

"explanation":""

}}

"""


        response=self.client.generate_structured_content(

            prompt,

            output_format="json",

            temperature=0.5

        )


        return self._convert_to_dict(response)







    def generate_explanation(
            self,
            question,
            answer
    ):


        prompt=f"""

Explain this answer:


Question:

{question}


Answer:

{answer}



Give detailed explanation.


"""


        return self.client.generate_text(prompt)







    def calculate_quiz_score(
            self,
            results:List[Dict]
    ):


        total_questions=len(results)


        correct_answers=sum(

            1

            for r in results

            if isinstance(r,dict)

            and r.get(
                "is_correct",
                False
            )

        )



        percentage=(

            correct_answers /

            total_questions *

            100

            if total_questions

            else 0

        )



        return {


            "total_questions":

                total_questions,


            "correct_answers":

                correct_answers,


            "incorrect_answers":

                total_questions-correct_answers,


            "percentage":

                round(
                    percentage,
                    2
                ),


            "score":

                correct_answers,


            "grade":

                self._get_grade(
                    percentage
                ),



            "performance":

                self._get_performance_message(
                    percentage
                )


        }






    @staticmethod
    def _get_grade(score):


        if score >= 90:
            return "A"


        elif score >=80:
            return "B"


        elif score>=70:
            return "C"


        elif score>=60:
            return "D"


        else:

            return "F"







    @staticmethod
    def _get_performance_message(score):


        if score>=90:

            return "🌟 Excellent! Outstanding performance!"


        elif score>=80:

            return "✅ Great! Very good understanding!"


        elif score>=70:

            return "👍 Good! Keep practicing!"


        elif score>=60:

            return "📚 Fair. Review and improve."


        else:

            return "💪 Need more practice. Keep learning!"