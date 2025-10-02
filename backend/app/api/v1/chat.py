from fastapi import APIRouter, Depends
from pydantic import BaseModel
import re
from sqlmodel import Session
from datetime import date as _date
from app.db.session import get_session, init_db
from app.db import crud
from app.services.ids import new_request_id
from app.temporal.client import get_client
from app.temporal.workflows.leave_request import LeaveRequestWorkflow, LeaveInput

router = APIRouter()

class ChatRequest(BaseModel):
  text: str

@router.on_event('startup')
async def _startup():
  init_db()

@router.post('/chat')
async def chat(req: ChatRequest, session: Session = Depends(get_session)):
  text = req.text.lower().strip()
  m = re.search(r'request leave (\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2})', text)
  if m:
    start_s, end_s = m.group(1), m.group(2)
    try:
      start = _date.fromisoformat(start_s)
      end = _date.fromisoformat(end_s)
    except Exception:
      return {"message": "Invalid date format. Use YYYY-MM-DD."}
    rid = new_request_id()
    crud.create_leave_request(session,
                              request_id=rid,
                              user_name='demo-user',
                              start_date=start,
                              end_date=end,
                              capacity='yellow')
    crud.add_audit(session, request_id=rid, actor='system', action='REQUEST_CREATED', details=f'{start_s} to {end_s}')
    # Start Temporal workflow
    client = get_client()
    handle = client.start_workflow(LeaveRequestWorkflow.run, LeaveInput(request_id=rid, user_name='demo-user', start_date=start_s, end_date=end_s), id=f"leave-{rid}", task_queue="leave-planner")
    _ = handle # silence linter in sync context
    return {
      "message": f"Request received for {start_s} to {end_s}. Pending review. I’ll remind your manager in ~48h.",
      "requestId": rid,
      "capacity": "yellow",
      "suggestions": [{"startDate": "2025-12-27", "endDate": "2025-12-29"}],
      "status": "PENDING_REVIEW"
    }
  if text.startswith('status '):
    rid = text.split(' ', 1)[1]
    lr = crud.get_leave_by_request_id(session, request_id=rid)
    if lr:
      return {"message": f"Status for {rid}: {lr.status}", "status": lr.status}
    return {"message": f"No request found for {rid}"}
  if text == 'pending':
    pending = crud.list_pending_requests(session)
    return {"message": f"You have {len(pending)} pending request(s).", "status": "PENDING_REVIEW"}
  if text.startswith('approve '):
    rid = text.split(' ', 1)[1]
    lr = crud.update_leave_status(session, request_id=rid, status='APPROVED')
    if lr:
      crud.add_audit(session, request_id=rid, actor='manager', action='APPROVED')
      return {"message": f"Approved {rid}.", "status": "APPROVED"}
    return {"message": f"No request found for {rid}"}
  return {"message": "Sorry, I didn't understand. Try: request leave 2025-12-10 to 2025-12-12"}
