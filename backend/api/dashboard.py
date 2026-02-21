import logging
import json
import asyncio
from datetime import datetime, timezone
from typing import AsyncGenerator, Union
from fastapi import APIRouter, Request, Body
from fastapi.responses import StreamingResponse
from backend.api.bus import dashboard_bus

from metra_classifier.main import classify_logs, correlate_logs

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/dashboard", tags=["dashboard"])

def _now() -> str:
    return datetime.now(tz=timezone.utc).strftime("%H:%M:%S")

# ── Endpoint: Push Data ────────────────────────────────────────────────────────

@router.post("/send_honeypot_json")
async def send_honeypot_json(data: Union[dict, list] = Body(...)):
    """
    Receives JSON or List of JSON and pushes items to all dashboard clients.
    Also triggers MITRE classification in the background.
    """
    subs = len(dashboard_bus.subscribers)
    
    if not isinstance(data, list):
        data = [data]

    # 1. Immediate Broadcast of raw logs
    count = 0
    for item in data:
        if isinstance(item, dict) and "timestamp" not in item:
            item["timestamp"] = _now()
        await dashboard_bus.emit(item)
        count += 1

    # 2. Background Classification
    async def run_and_emit_classification(log_data):
        logger.info(f"Background classification task started for {len(log_data)} logs.")
        try:
            # results is now a List[dict]
            results = await classify_logs(log_data)
            if results:
                for res in results:
                    res["timestamp"] = _now()
                    await dashboard_bus.emit(res)
                logger.info(f"Emitted {len(results)} individual classifications.")
            else:
                logger.warning("Classification results was empty or None.")

            # 2. Correlation (Multi-stage Analysis)
            correlation = await correlate_logs(log_data)
            if correlation:
                if "timestamp" not in correlation:
                    correlation["timestamp"] = _now()
                if "detected_at" not in correlation:
                    correlation["detected_at"] = _now()
                await dashboard_bus.emit(correlation)
                logger.info("Attack correlation emitted to dashboard bus.")

        except Exception as e:
            logger.error(f"Classification background task failed: {e}", exc_info=True)

    # Fire and forget
    asyncio.create_task(run_and_emit_classification(data))

    return {"status": "broadcasted", "items": count, "subscribers": subs}

# ── Endpoint: Consolidated Stream ──────────────────────────────────────────────

@router.get("/stream")
async def stream_dashboard_events(request: Request):
    """
    A single SSE stream that pushes all dashboard-related notifications.
    """
    queue = await dashboard_bus.subscribe()
    client_ip = request.client.host if request.client else "unknown"
    logger.info(f"New dashboard subscriber connected from {client_ip}. Total: {len(dashboard_bus.subscribers)}")

    async def event_generator():
        try:
            while True:
                if await request.is_disconnected():
                    logger.info(f"Dashboard client {client_ip} disconnected.")
                    break
                
                try:
                    # Use a timeout so we can check for disconnection periodically
                    msg = await asyncio.wait_for(queue.get(), timeout=1.0)
                    yield msg
                except asyncio.TimeoutError:
                    continue
        except Exception as e:
            logger.error(f"Error in dashboard stream for {client_ip}: {e}")
        finally:
            dashboard_bus.unsubscribe(queue)
            logger.info(f"Unsubscribed client {client_ip}. Remaining: {len(dashboard_bus.subscribers)}")

    return StreamingResponse(event_generator(), media_type="text/event-stream")

# We'll need to start this simulator somewhere, or keep it in dashboard.py 
# for convenience. main.py is better for lifecycle management.
