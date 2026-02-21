import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def get_llm_response(prompt: str, model: str = "gemini-2.5-flash-lite") -> str:
    """
    Invokes the Gemini LLM with the given prompt and returns the text response.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
    llm = ChatGoogleGenerativeAI(model=model, google_api_key=api_key)
    response = llm.invoke(prompt)
    return response.content
