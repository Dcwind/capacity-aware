from fastapi import APIRouter
from pydantic import BaseModel
from typing import Literal

router = APIRouter()

# In-memory store for demo
PENDING: list[dict] = [
    {"request_id": "req_demo_123", "name": "Jane Doe", "start": "2025-12-10", "end": "2025-12-12", "status": "PENDING", "age": 0}
]

class Decision(BaseModel):
    request_id: str
    decision: Literal['APPROVE', 'REJECT']
    note: str | None = None

@router.get('/pending')
async def list_pending():
    return {"items": PENDING}

@router.post('/decision')
async def manager_decision(d: Decision):
    for item in PENDING:
        if item["request_id"] == d.request_id:
            item["status"] = d.decision
            return {"ok": True, "request_id": d.request_id, "status": d.decision}
    return {"ok": False}
