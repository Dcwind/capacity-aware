from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Literal
from sqlmodel import Session
from app.db.session import get_session
from app.db import crud

router = APIRouter()

class Decision(BaseModel):
    request_id: str
    decision: Literal['APPROVE', 'REJECT']
    note: str | None = None

@router.get('/pending')
async def list_pending(session: Session = Depends(get_session)):
    items = crud.list_pending_requests(session)
    # shape for UI table
    return {"items": [
        {
            "request_id": it.request_id,
            "name": it.user_name,
            "start": str(it.start_date),
            "end": str(it.end_date),
            "status": it.status,
            "age": 0,
        } for it in items
    ]}

@router.post('/decision')
async def manager_decision(d: Decision, session: Session = Depends(get_session)):
    new_status = 'APPROVED' if d.decision == 'APPROVE' else 'REJECTED'
    lr = crud.update_leave_status(session, request_id=d.request_id, status=new_status)
    if not lr:
        return {"ok": False}
    crud.add_audit(session, request_id=d.request_id, actor='manager', action=new_status, details=d.note)
    return {"ok": True, "request_id": d.request_id, "status": new_status}
