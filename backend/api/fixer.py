import json
import asyncio
import logging
from fastapi import APIRouter, Request, Body
from fastapi.responses import StreamingResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/fixing", tags=["fixing"])

@router.get("/stream")
async def stream_fixer_status(request: Request):
    """
    SSE endpoint for tracking the Fixer Agent remediation steps.
    """
    async def fixer_generator():
        while True:
            if await request.is_disconnected():
                logger.info("Client disconnected from /fixing/stream")
                break
                
            demo_data = {
                "type": "node_start",
                "node": "fixer_agent",
                "status": "remediating_vulnerability",
                "file": "server.js"
            }
            yield f"data: {json.dumps(demo_data)}\n\n"
            await asyncio.sleep(4)

    return StreamingResponse(fixer_generator(), media_type="text/event-stream")

@router.post("/remediate")
async def trigger_remediation(payload: dict = Body(...)):
    """
    Endpoint to trigger a fixing workflow for a specific vulnerability.
    """
    logger.info(f"Triggering remediation for: {payload}")
    return {"status": "started", "task_id": "fix_123"}
