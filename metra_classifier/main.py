import asyncio
import json
from typing import Optional, Any
from google import genai
import re

from prompts import SYSTEM_PROMPT, OUTPUT_SCHEMA
from env_setup import *

# -------------------------
# Gemini client setup
# -------------------------
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in environment variables.")
client = genai.Client(api_key=GEMINI_API_KEY)

# -------------------------
# Utilities
# -------------------------
async def read_from_json(path: str) -> Optional[Any]:
    logger.info(f"Reading {path}")
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed reading {path}: {e}")
        return None


# optional normalization step for logs - can add ECS / OSSEM rules here later
async def logs_normalization(logs: Any) -> Any:
    if isinstance(logs, list):
        for event in logs:
            if "timestamp" in event:
                event["timestamp"] = str(event["timestamp"])

    return logs


def clean_llm_json(text: str) -> str:
    text = text.strip()

    # Remove json or  wrappers
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    return text.strip()


# -------------------------
# LLM Classification
# -------------------------

async def classify_with_gemini(logs: Any, mitre_data: Any) -> Optional[dict]:
    logger.info("Calling Gemini classifier")

    logs_str = json.dumps(logs)
    mitre_str = json.dumps(mitre_data)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=(
                SYSTEM_PROMPT +
                OUTPUT_SCHEMA +
                f"\nLOGS:\n{logs_str}\n\n"
                f"MITRE ATT&CK DATA:\n{mitre_str}"
            )
        )

        raw_output = response.text
        logger.info("LLM response received")

        cleaned_output = clean_llm_json(raw_output)

        logger.info("Parsing LLM JSON")
        parsed_json = json.loads(cleaned_output)

        return parsed_json

    except json.JSONDecodeError as e:
        logger.error("JSON parsing failed")
        logger.error(f"Raw LLM output:\n{raw_output}")
        logger.error(f"Error: {e}")
        return None

    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return None


# -------------------------
# Workflow
# -------------------------

async def run_classification_workflow(
    honeypot_logs_path: str,
    mitre_attack_path: str
):
    logger.info("Starting classification workflow")

    honeypot_logs = await read_from_json(honeypot_logs_path)
    mitre_attack = await read_from_json(mitre_attack_path)

    if not honeypot_logs:
        logger.error("Missing honeypot logs")
        return

    if not mitre_attack:
        logger.error("Missing MITRE ATT&CK dataset")
        return

    normalized_logs = await logs_normalization(honeypot_logs)

    classification_result = await classify_with_gemini(
        normalized_logs,
        mitre_attack
    )

    if classification_result:
        logger.info("Classification successful")
        print(json.dumps(classification_result, indent=4))
    else:
        logger.error("Classification failed")


# -------------------------
# Entry Point
# -------------------------

async def runner():
    logger.info("MITRE ATT&CK classification program started")

    await run_classification_workflow(
        "data/honeypot_logs.json",
        "data/mitre_attack.json"
    )

    logger.info("Classification workflow completed")


if __name__ == "__main__":
    asyncio.run(runner())