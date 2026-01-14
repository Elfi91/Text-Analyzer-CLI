
import sys
import os

# Add project root to sys.path to allow importing from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ai_client import analyze_sentiment

def main():
    print("--- Verifying Gemini API Integration ---")
    
    test_text = "This is a fantastic feature, I really enjoy using it!"
    print(f"Input Text: '{test_text}'")
    
    print("\nSending request to Gemini...")
    result = analyze_sentiment(test_text)
    
    print(f"\nResponse Received:\n{result}")
    
    if result.get("sentiment") == "POSITIVE":
        print("\n✅ SUCCESS: Sentiment correctly identified as POSITIVE.")
    elif result.get("sentiment") == "ERROR" or result.get("sentiment") == "API ERROR":
        print("\n❌ FAILURE: API Error occurred. Check your API Key and internet connection.")
    else:
        print(f"\n⚠️ UNEXPECTED: Result {result} was not explicitly POSITIVE as expected for this text.")

if __name__ == "__main__":
    main()
