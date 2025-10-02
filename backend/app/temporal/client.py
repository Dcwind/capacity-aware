from __future__ import annotations
import asyncio
from functools import lru_cache
from temporalio.client import Client

@lru_cache(maxsize=1)
def get_event_loop() -> asyncio.AbstractEventLoop:
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop

@lru_cache(maxsize=1)
def get_client() -> Client:
    loop = get_event_loop()
    return loop.run_until_complete(Client.connect("localhost:7233"))
