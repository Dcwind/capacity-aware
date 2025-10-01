from fastapi import APIRouter
from pydantic import BaseModel
import re

router = APIRouter()

class ChatRequest(BaseModel):
  text: str

@router.post('/chat')
async def chat(req: ChatRequest):
  text = req.text.lower().strip()
  m = re.search(r'request leave (\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2})', text)
  if m:
    start, end = m.group(1), m.group(2)
    return {
      "message": f"Request received for {start} to {end}. Pending review. I’ll remind your manager in ~48h.",
      "requestId": "req_demo_123",
      "capacity": "yellow",
      "suggestions": [{"startDate": "2025-12-27", "endDate": "2025-12-29"}],
      "status": "PENDING_REVIEW"
    }
  if text.startswith('status '):
    rid = text.split(' ', 1)[1]
    return {"message": f"Status for {rid}: PENDING_REVIEW", "status": "PENDING_REVIEW"}
  if text == 'pending':
    return {"message": "You have 1 pending request.", "status": "PENDING_REVIEW"}
  if text.startswith('approve '):
    rid = text.split(' ', 1)[1]
    return {"message": f"Approved {rid}.", "status": "APPROVED"}
  return {"message": "Sorry, I didn't understand. Try: request leave 2025-12-10 to 2025-12-12"}
