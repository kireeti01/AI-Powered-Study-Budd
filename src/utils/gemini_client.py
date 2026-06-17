"""
Groq API Client
"""

from groq import Groq
from typing import Optional, List
import logging
import os
import json
from src.config.settings import ERROR_MESSAGES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeminiClient:
    """
    Groq client with Gemini-compatible function names
    """

    def __init__(self, api_key: Optional[str] = None):

        self.api_key = api_key or os.getenv("GROQ_API_KEY")

        if not self.api_key:
            raise ValueError(
                "Groq API key missing"
            )

        try:
            self.client = Groq(
                api_key=self.api_key
            )

            logger.info(
                "✅ Groq API connected successfully"
            )

        except Exception as e:
            logger.error(str(e))
            raise ValueError(str(e))


    def generate_text(
        self,
        prompt: str,
        temperature=0.7,
        max_tokens=2000,
        system_prompt=None
    ):

        try:

            messages = []

            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })


            messages.append({
                "role": "user",
                "content": prompt
            })


            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )


            return response.choices[0].message.content


        except Exception as e:

            logger.error(
                f"❌ API Error: {str(e)}"
            )

            raise Exception(
                f"{ERROR_MESSAGES['api_error']}\nDetails: {str(e)}"
            )



    def generate_structured_content(
        self,
        prompt: str,
        output_format: str = "json",
        temperature: float = 0.5
    ) -> dict:

        try:

            structured_prompt = f"""
{prompt}

IMPORTANT:
Return only {output_format} format.
Do not add explanations.
"""


            response_text = self.generate_text(
                structured_prompt,
                temperature=temperature
            )


            if output_format.lower() == "json":

                try:

                    return json.loads(response_text)


                except json.JSONDecodeError:

                    if "```json" in response_text:

                        json_text = (
                            response_text
                            .split("```json")[1]
                            .split("```")[0]
                        )

                        return json.loads(json_text)


                    return {
                        "response": response_text
                    }


            return {
                "response": response_text
            }


        except Exception as e:

            logger.error(
                f"❌ Structured content error: {str(e)}"
            )

            return {
                "error": str(e)
            }



    def generate_with_context(
        self,
        prompt,
        context,
        system_prompt=None,
        temperature=0.5
    ):


        full_prompt = f"""
Context:
{context}


Question:
{prompt}


Answer based on the context.
"""


        return self.generate_text(
            full_prompt,
            temperature=temperature,
            system_prompt=system_prompt
        )



    def generate_batch(
        self,
        prompts: List[str]
    ):

        responses = []

        for prompt in prompts:

            responses.append(
                self.generate_text(prompt)
            )


        return responses



    def verify_api_connection(self):

        try:

            response = self.generate_text(
                "Reply only OK"
            )

            return bool(response)


        except Exception:

            return False




_gemini_client = None



def get_gemini_client():

    global _gemini_client


    if _gemini_client is None:

        _gemini_client = GeminiClient()


    return _gemini_client