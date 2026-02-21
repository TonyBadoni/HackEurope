import sys
import os

# Add the parent directory to sys.path to allow importing from llm
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm.api_call import get_llm_response

def test_gemini_api():
    print("Testing Gemini API connection...")
    try:
        response = get_llm_response("Hello! How is your day today.")
        print("-" * 30)
        print(f"Response: {response}")
        print("-" * 30)
        if "API Connection Successful" in response:
            print("✅ Success! Your Google Gemini API key is working correctly.")
        else:
            print("⚠️ Received a response, but it didn't match the expected string.")
            print("This usually means the API is working but the response was different.")
    except Exception as e:
        print("❌ Error testing API:")
        print(str(e))
        print("\nPlease check:")
        print("1. Your GOOGLE_API_KEY is correct in the .env file.")
        print("2. You have internet connectivity.")
        print("3. You have 'langchain-google-genai' and 'python-dotenv' installed.")

if __name__ == "__main__":
    test_gemini_api()
