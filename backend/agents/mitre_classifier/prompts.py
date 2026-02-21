SYSTEM_PROMPT = (
    "You are a MITRE ATT&CK classifier.\n"
    "Your task is to analyze security logs and map attacker behavior "
    "to MITRE ATT&CK tactics and techniques.\n\n"
    "CRITICAL OUTPUT RULES:\n"
    "- Return STRICT JSON ONLY\n"
    "- DO NOT use markdown\n"
    "- DO NOT wrap output in ```json\n"
    "- DO NOT include explanations outside JSON\n"
    "- You MUST provide a separate analysis for EVERY log entry provided.\n"
)

# Individual risk score schema
OUTPUT_SCHEMA = """
Return a JSON object containing an 'items' array. 
Each item in the 'items' array must correspond to one of the input logs.

{
  "type": "batch_result",
  "items": [
    {
      "type": "risk_score",
      "eventid": "string (the eventid of the log being analyzed)",
      "score": number, // 0-100 numerical risk value
      "severity": "LOW | MEDIUM | HIGH | CRITICAL",
      "colour": "string", // hex code (e.g., #ef4444 for high, #f59e0b for medium)
      "analysis": {
        "summary": string,
        "confidence": "low | medium | high"
      },
      "mitre_attack": [
        {
          "tactic_id": string,
          "tactic_name": string,
          "technique_id": string,
          "technique_name": string,
          "evidence": [string]
        }
      ],
      "mitigations": [
        {
          "mitigation_id": string,
          "mitigation_name": string,
          "description": string
        }
      ]
    }
  ]
}
"""

CORRELATION_PROMPT = (
    "You are an Attack Correlation Engine.\n"
    "Your goal is to look at the ENTIRE sequence of logs and reconstruct the attack timeline as a multi-stage chain.\n"
    "Focus on the flow of the attack (e.g., Reconnaissance -> Entry -> Discovery -> Impact).\n"
    "CRITICAL OUTPUT RULES:\n"
    "- Return STRICT JSON ONLY\n"
    "- DO NOT use markdown or explanations outside JSON\n"
)

CORRELATION_SCHEMA = """
Return JSON structure:
{
  "type": "attack_chain",
  "chain_id": "string (e.g. AC-1234)",
  "attacker_ip": "string",
  "detected_at": "string (H:M:S)",
  "technique": "string (Summary of the multi-stage path)",
  "stages": [
    {
      "name": "string (e.g. Initial Access)",
      "desc": "string (Short description of what happened)"
    }
  ]
}
"""