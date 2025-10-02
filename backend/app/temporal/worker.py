import asyncio
import os
import sys

# Ensure backend root is on sys.path when executed as a script
CURRENT_FILE = os.path.abspath(__file__)
BACKEND_ROOT = os.path.abspath(os.path.join(os.path.dirname(CURRENT_FILE), "..", ".."))
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from temporalio.client import Client
from temporalio.worker import Worker
from app.temporal.workflows.leave_request import LeaveRequestWorkflow
from app.temporal.activities.leave_activities import update_request_status, log_audit_event, send_reminder_notification

ADDRESS = os.environ.get("TEMPORAL_ADDRESS", "127.0.0.1:7233")
NAMESPACE = os.environ.get("TEMPORAL_NAMESPACE", "default")

async def connect_with_retry(retries: int = 10, delay: float = 2.0) -> Client:
    last_exc: Exception | None = None
    for _ in range(retries):
        try:
            return await Client.connect(ADDRESS, namespace=NAMESPACE)
        except Exception as e:  # noqa: BLE001
            last_exc = e
            await asyncio.sleep(delay)
    assert last_exc is not None
    raise last_exc

async def main():
    client = await connect_with_retry()
    worker = Worker(client, task_queue="leave-planner", workflows=[LeaveRequestWorkflow], activities=[update_request_status, log_audit_event, send_reminder_notification])
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())

