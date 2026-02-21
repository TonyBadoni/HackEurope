import asyncio
import json
from typing import Set

class EventBus:
    def __init__(self):
        self.subscribers: Set[asyncio.Queue] = set()

    async def subscribe(self) -> asyncio.Queue:
        queue = asyncio.Queue()
        self.subscribers.add(queue)
        return queue

    def unsubscribe(self, queue: asyncio.Queue):
        if queue in self.subscribers:
            self.subscribers.remove(queue)

    async def emit(self, data: dict):
        if not self.subscribers:
            # logger.info("No active subscribers, skipping broadcast.")
            return
            
        message = f"data: {json.dumps(data)}\n\n"
        # Create tasks to avoid blocking if one queue is slow
        tasks = [asyncio.create_task(queue.put(message)) for queue in self.subscribers]
        if tasks:
            await asyncio.wait(tasks)
            # logger.info(f"Broadcasted message to {len(tasks)} subscribers.")

# Global instances for the specific streams
# We could use one bus or multiple. The user wants a consolidated stream, 
# so one bus is better.
dashboard_bus = EventBus()
