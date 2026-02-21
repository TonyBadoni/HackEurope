import asyncio
import os
import sys
import json
from dotenv import load_dotenv

# Add project root to path just in case
sys.path.append(os.getcwd())

async def diagnose():
    print("--- Environment Diagnosis ---")
    print(f"Python Version: {sys.version}")
    print(f"Current Working Directory: {os.getcwd()}")
    
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    print(f"GEMINI_API_KEY present: {'Yes' if api_key else 'No'}")
    
    print("\n--- Testing Imports ---")
    try:
        import google.generativeai as genai
        print("SUCCESS: import google.generativeai")
    except ImportError as e:
        print(f"FAILURE: import google.generativeai -> {e}")
        
    try:
        from metra_classifier.main import classify_logs
        print("SUCCESS: from metra_classifier.main import classify_logs")
    except ImportError as e:
        print(f"FAILURE: from metra_classifier.main import classify_logs -> {e}")
    except Exception as e:
        print(f"FAILURE during import: {e}")

    print("\n--- Testing Classification Logic ---")
    if 'classify_logs' in locals():
        test_logs = [{"eventid": "test", "message": "Health check", "src_ip": "1.1.1.1"}]
        try:
            print("Running test classification (this may take a few seconds)...")
            # We skip the actual LLM call if the key is missing to avoid hanging or erroring out
            if not api_key:
                print("Skipping LLM call due to missing API key.")
            else:
                result = await classify_logs(test_logs)
                if result:
                    print("SUCCESS: Classification result received.")
                    print(json.dumps(result, indent=2))
                else:
                    print("FAILURE: Classification returned None.")
        except Exception as e:
            print(f"FAILURE during classification: {e}")

if __name__ == "__main__":
    asyncio.run(diagnose())
