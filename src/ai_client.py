
"""
Module for interacting with Google's Gemini API.
Handles authentication, prompt construction, and error handling via GeminiClient class.
"""
import os
import logging
import json
import google.generativeai as genai
from google.api_core import exceptions
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class GeminiClient:
    """Class to manage interactions with Gemini AI."""

    def __init__(self, api_key: str = None, model_name: str = "gemini-flash-latest"):
        """
        Initializes the Gemini Client.

        Args:
            api_key (str): The Gemini API Key. If None, tries to load from env.
            model_name (str): The model to use.
        """
        load_dotenv()
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name

        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found.")
        else:
            genai.configure(api_key=self.api_key)

    def analyze_sentiment(self, text: str) -> dict:
        """
        Analyzes the sentiment of the text using Gemini API.
        """
        if not self.api_key:
            logger.error("Attempted analysis without API Key.")
            return {"sentiment": "ERROR", "confidence": "None"}

        try:
            model = genai.GenerativeModel(self.model_name)
            
            prompt = (
                f"Analyze the sentiment of the following text: '{text}'.\n"
                "Respond STRICTLY in the following JSON format:\n"
                "{\"sentiment\": \"POSITIVE\" | \"NEGATIVE\" | \"NEUTRAL\", \"confidence\": \"HIGH\" | \"MEDIUM\" | \"LOW\"}\n"
                "Do not include any other text or markdown formatting."
            )

            logger.debug(f"Sending request to Gemini: {text[:50]}...")
            
            try:
                response = model.generate_content(prompt)
                
                if response.prompt_feedback.block_reason:
                     logger.warning(f"Response blocked: {response.prompt_feedback}")
                     return {"sentiment": "BLOCKED", "confidence": "Filters Triggered"}

                response_text = response.text.strip()
                logger.debug(f"Received raw response: {response_text}")

            except ValueError:
                logger.error("Gemini response empty/blocked.")
                return {"sentiment": "AI_ERROR", "confidence": "Content Blocked"}

            # Basic cleanup if model wraps in ```json ... ```
            if response_text.startswith("```"):
                lines = response_text.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines[-1].startswith("```"):
                    lines = lines[:-1]
                response_text = "\n".join(lines).strip()

            result = json.loads(response_text)
            
            if "sentiment" not in result or "confidence" not in result:
                 raise ValueError("Missing keys in JSON response")
                 
            return result

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            return {"sentiment": "UNKNOWN", "confidence": "Low - Parse Error"}
            
        except exceptions.GoogleAPIError as e:
            logger.error(f"Gemini API Error: {e}")
            return {"sentiment": "API ERROR", "confidence": "None"}
            
        except Exception as e:
            logger.error(f"Unexpected AI Error: {e}")
            return {"sentiment": "ERROR", "confidence": "None"}

    def generate_summary(self, text: str) -> str:
        """
        Generates a concise summary of the text using Gemini.
        """
        if not self.api_key:
            return "AI Summary Unavailable (No Key)"

        try:
            model = genai.GenerativeModel(self.model_name)
            
            prompt = (
                f"Summarize the following text in 2-3 concise sentences: '{text[:10000]}'.\n" 
                "Keep it plain text."
            )

            logger.debug(f"Requesting summary for text length {len(text)}...")
            response = model.generate_content(prompt)
            
            if response.text:
                return response.text.strip()
            else:
                return "No summary generated."

        except Exception as e:
            logger.error(f"Summary generation failed: {e}")
            return "Summary Error"
