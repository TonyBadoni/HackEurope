from dotenv import load_dotenv
import os
import logging

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

logging.basicConfig(
    filename="classification.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)
