from pathlib import Path
from dotenv import load_dotenv
import os
import logging

# Robust path resolution for .env
project_root = Path(__file__).resolve().parents[3]  # HackEurope root
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path)

# Support both GEMINI_API_KEY and GOOGLE_API_KEY
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

logging.basicConfig(
    filename="classification.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)
