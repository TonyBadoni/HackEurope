import asyncio
import json
import os
from typing import Optional, Any, List
from google import genai
import re
import logging

# Ensure env variables are loaded
from metra_classifier.env_setup import logger, GEMINI_API_KEY
from metra_classifier.prompts import (
    SYSTEM_PROMPT, 
    OUTPUT_SCHEMA, 
    CORRELATION_PROMPT, 
    CORRELATION_SCHEMA
)

# -------------------------
# Gemini client setup
# -------------------------
client = None
if GEMINI_API_KEY:
    logger.info(f"Metra Classifier: Configuring Gemini with key starting with {GEMINI_API_KEY[:8]}")
    try:
        # Use the newer google-genai SDK
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        logger.error(f"Metra Classifier: Failed to initialize Gemini Client: {e}")
else:
    logger.error("Metra Classifier: MISSING API KEY. Gemini will NOT work.")

# Global cache for MITRE data
_cached_mitre_data = None

# -------------------------
# Utilities
# -------------------------
def get_mitre_data(path: str = "data/mitre_attack.json") -> Optional[Any]:
    global _cached_mitre_data
    if _cached_mitre_data is not None:
        return _cached_mitre_data
    
    possible_paths = [
        path,
        os.path.join(os.getcwd(), path),
        os.path.join(os.path.dirname(__file__), "..", "..", path), 
        "/home/bigbouncyboii/hackathon/HackEurope/data/mitre_attack.json"
    ]
    
    for p in possible_paths:
        if os.path.exists(p):
            try:
                with open(p, "r") as f:
                    _cached_mitre_data = json.load(f)
                    logger.info(f"Metra Classifier: Loaded MITRE data from {p}")
                    return _cached_mitre_data
            except Exception as e:
                logger.error(f"Metra Classifier: Failed loading MITRE data from {p}: {e}")
    
    logger.error(f"Metra Classifier: MITRE data not found. Tried paths: {possible_paths}")
    return None

async def logs_normalization(logs: Any) -> Any:
    if isinstance(logs, list):
        for event in logs:
            if isinstance(event, dict) and "timestamp" in event:
                event["timestamp"] = str(event["timestamp"])
    return logs

def clean_llm_json(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()

# -------------------------
# LLM Classification
# -------------------------

async def classify_with_gemini(logs: List[dict], mitre_data: Any) -> Optional[dict]:
    if not client:
        logger.error("Metra Classifier: Gemini client not initialized.")
        return None

    logger.info(f"Metra Classifier: Sending {len(logs)} logs to Gemini for classification")
    logs_str = json.dumps(logs)
    mitre_str = json.dumps(mitre_data)

    try:
        prompt = (
            SYSTEM_PROMPT +
            "\n" + OUTPUT_SCHEMA +
            f"\nLOGS:\n{logs_str}\n\n"
            f"MITRE ATT&CK DATA:\n{mitre_str}"
        )
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        raw_output = response.text
        cleaned_output = clean_llm_json(raw_output)
        parsed_json = json.loads(cleaned_output)

        # Handle batch results or single result
        results = []
        if isinstance(parsed_json, dict) and "items" in parsed_json:
            results = parsed_json["items"]
        else:
            results = [parsed_json]

        # Post-process each item for dashboard compatibility
        attacker_ip = None
        if logs and isinstance(logs, list) and len(logs) > 0:
            attacker_ip = logs[0].get("src_ip")

        for item in results:
            if not isinstance(item, dict): continue
            
            # Inject attacker IP
            if attacker_ip:
                item["attacker_ip"] = attacker_ip
            
            # Flatten summary for dashboard
            if "analysis" in item and "summary" in item["analysis"]:
                item["summary"] = item["analysis"]["summary"]
            
            # Ensure type is set
            if "type" not in item:
                item["type"] = "risk_score"

        return results

    except Exception as e:
        logger.error(f"Metra Classifier: Exception during LLM call/parse: {e}", exc_info=True)
        return None

async def correlate_with_gemini(logs: List[dict]) -> Optional[dict]:
    if not client:
        return None

    logger.info(f"Metra Classifier: Correlating {len(logs)} logs")
    logs_str = json.dumps(logs)

    try:
        prompt = (
            CORRELATION_PROMPT +
            "\n" + CORRELATION_SCHEMA +
            f"\nLOGS:\n{logs_str}"
        )
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        if not response or not response.text:
            return None

        raw_output = response.text
        cleaned_output = clean_llm_json(raw_output)
        parsed_json = json.loads(cleaned_output)

        if logs and isinstance(logs, list) and len(logs) > 0:
            first_log = logs[0]
            if isinstance(first_log, dict) and "src_ip" in first_log:
                parsed_json["attacker_ip"] = first_log["src_ip"]

        return parsed_json

    except Exception as e:
        logger.error(f"Metra Classifier: Exception during correlation: {e}")
        return None

async def classify_logs(logs: List[dict]) -> Optional[dict]:
    """
    Main entry point for classifying a batch of logs.
    """
    logger.info("Metra Classifier: classify_logs called")
    mitre_data = get_mitre_data()
    if not mitre_data:
        return None
    
    normalized = await logs_normalization(logs)
    return await classify_with_gemini(normalized, mitre_data)

async def correlate_logs(logs: List[dict]) -> Optional[dict]:
    """
    Main entry point for correlating a batch of logs into an attack chain.
    """
    logger.info("Metra Classifier: correlate_logs called")
    normalized = await logs_normalization(logs)
    return await correlate_with_gemini(normalized)

# -------------------------
# Workflow (Legacy/CLI support)
# -------------------------

async def runner():
    logger.info("Metra Classifier: CLI Runner started")
    test_logs = [{"eventid": "cowrie.login.success", "src_ip": "1.2.3.4", "message": "Test login"}]
    
    print("--- Classification ---")
    result = await classify_logs(test_logs)
    if result:
        print(json.dumps(result, indent=4))
    
    print("\n--- Correlation ---")
    corr = await correlate_logs(test_logs)
    if corr:
        print(json.dumps(corr, indent=4))

if __name__ == "__main__":
    asyncio.run(runner())