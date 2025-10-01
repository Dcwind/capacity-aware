from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.db import crud

router = APIRouter()

@router.get('/status/{request_id}')
async def get_status(request_id: str, session: Session = Depends(get_session)):
    lr = crud.get_leave_by_request_id(session, request_id=request_id)
    if not lr:
        return {"request_id": request_id, "status": "NOT_FOUND"}
    return {"request_id": request_id, "status": lr.status}
