import logging
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from llm.api_call import get_llm_response

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/rules", tags=["rules"])

class RuleGenerationRequest(BaseModel):
    prompt: str
    template: str

class RuleDeploymentRequest(BaseModel):
    xml_content: str
    rule_name: str

@router.post("/generate")
async def generate_rule_xml(request: RuleGenerationRequest):
    # ... (previous code same)
    try:
        system_prompt = f"""
        You are a security expert specialized in Wazuh XML rules.
        Your task is to generate a valid Wazuh XML rule based on the user's natural language request.
        
        RULSET CONTEXT:
        The user is starting with this base template:
        {request.template}
        
        USER REQUEST:
        {request.prompt}
        
        INSTRUCTIONS:
        1. Return ONLY the valid XML inside <rule> tags.
        2. Ensure the XML structure is correct.
        3. Assign a custom rule ID (e.g., 100001 or incremented).
        4. No explanation or code blocks, just the XML content itself.
        """
        
        xml_response = get_llm_response(system_prompt)
        
        # Clean up possible markdown if LLM includes it
        if "```xml" in xml_response:
            xml_response = xml_response.split("```xml")[1].split("```")[0].strip()
        elif "```" in xml_response:
            xml_response = xml_response.split("```")[1].split("```")[0].strip()
            
        return {"xml": xml_response.strip()}
        
    except Exception as e:
        logger.error(f"Error generating rule: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/deploy")
async def deploy_rule(request: RuleDeploymentRequest):
    """
    Saves the generated XML rule to the wazuh-rules directory.
    This directory is mapped as a volume in Docker Compose.
    """
    try:
        import os
        # Path inside container
        rules_dir = "/app/wazuh-rules"
        if not os.path.exists(rules_dir):
            # Fallback for local development
            rules_dir = "wazuh-rules"
            os.makedirs(rules_dir, exist_ok=True)
            
        # Standard Wazuh rule file naming
        file_path = os.path.join(rules_dir, "local_rules.xml")
        
        # In a real app we might append or manage multiple files, 
        # but for a hackathon we'll wrap it in <group name="local,">
        # unless it already has it.
        
        xml_to_save = request.xml_content
        if "<group name=" not in xml_to_save:
            xml_to_save = f'<group name="local,">\n{xml_to_save}\n</group>'
            
        with open(file_path, "w") as f:
            f.write(xml_to_save)
            
        return {"status": "success", "path": file_path}
        
    except Exception as e:
        logger.error(f"Error deploying rule: {e}")
        raise HTTPException(status_code=500, detail=str(e))
