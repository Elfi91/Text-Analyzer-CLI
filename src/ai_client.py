
"""
Module for interacting with Google's Gemini API.
Handles authentication, prompt construction, and error handling.
"""
import os
import logging
import json
import google.generativeai as genai
from google.api_core import exceptions
from dotenv import load_dotenv

# Load environment variables (e.g., GEMINI_API_KEY)
load_dotenv()

logger = logging.getLogger(__name__)

# Configure Gemini with the API Key
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    logger.warning("GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=API_KEY)

# Use a lightweight model for speed
MODEL_NAME = "gemini-flash-latest"

def analyze_sentiment(text: str) -> dict:
    """
    Analyzes the sentiment of the text using Gemini API.

    Args:
        text (str): The text to analyze.

    Returns:
        dict: A dictionary containing 'sentiment' (POSITIVE, NEGATIVE, NEUTRAL)
              and 'confidence' (High/Medium/Low).
              Returns default error values if the call fails.
    """
    if not API_KEY:
        logger.error("Attempted analysis without API Key.")
        return {"sentiment": "ERROR", "confidence": "None"}

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        
        # Structured Prompt Engineering
        prompt = (
            f"Analyze the sentiment of the following text: '{text}'.\n"
            "Respond STRICTLY in the following JSON format:\n"
            "{\"sentiment\": \"POSITIVE\" | \"NEGATIVE\" | \"NEUTRAL\", \"confidence\": \"HIGH\" | \"MEDIUM\" | \"LOW\"}\n"
            "Do not include any other text or markdown formatting."
        )

        logger.debug(f"Sending request to Gemini: {text[:50]}...")
        
        try:
            response = model.generate_content(prompt)
            
            # Check for block due to safety/copyright/etc
            if response.prompt_feedback.block_reason:
                 logger.warning(f"Response blocked: {response.prompt_feedback}")
                 return {"sentiment": "BLOCKED", "confidence": "Filters Triggered"}

            response_text = response.text.strip()
            logger.debug(f"Received raw response: {response_text}")

        except ValueError:
            # response.text raises ValueError if content was blocked but block_reason wasn't caught above
            logger.error("Gemini response empty/blocked (likely Safety or Recitation).")
            return {"sentiment": "AI_ERROR", "confidence": "Content Blocked"}

        # Basic cleanup if model wraps in ```json ... ```
        if response_text.startswith("```"):
            # Remove markedown code blocks
            lines = response_text.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            response_text = "\n".join(lines).strip()


        result = json.loads(response_text)
        
        # Validate keys
        if "sentiment" not in result or "confidence" not in result:
             raise ValueError("Missing keys in JSON response")
             
        return result

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse AI response as JSON: {e}\nResponse text was: {response_text}")
        return {"sentiment": "UNKNOWN", "confidence": "Low - Parse Error"}
        
    except exceptions.GoogleAPIError as e:
        logger.error(f"Gemini API Error: {e}")
        return {"sentiment": "API ERROR", "confidence": "None"}
        
    except Exception as e:
        logger.error(f"Unexpected error in analyze_sentiment: {e}")
        return {"sentiment": "ERROR", "confidence": "None"}
