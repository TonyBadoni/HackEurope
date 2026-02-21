import json
import asyncio
import logging
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/classification", tags=["classification"])

@router.get("/stream")
async def stream_mitre_classifications(request: Request):
    """
    SSE endpoint for MITRE ATT&CK classifications.
    """
    async def classification_generator():
        while True:
            if await request.is_disconnected():
                logger.info("Client disconnected from /classification/stream")
                break
                
            demo_data = {
                "type": "mitre_classification",
                "technique_id": "T1059.004",
                "technique_name": "Command and Scripting Interpreter: Unix Shell",
                "severity": "High",
                "confidence": 0.95
            }
            yield f"data: {json.dumps(demo_data)}\n\n"
            await asyncio.sleep(5)

    return StreamingResponse(classification_generator(), media_type="text/event-stream")
