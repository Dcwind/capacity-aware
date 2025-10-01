import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

# Placeholders for workflows/activities once implemented

async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(client, task_queue="leave-planner", workflows=[], activities=[])
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())

