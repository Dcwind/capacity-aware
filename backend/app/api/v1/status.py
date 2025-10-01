from fastapi import APIRouter

router = APIRouter()

@router.get('/status/{request_id}')
async def get_status(request_id: str):
    # Demo: fixed status
    return {"request_id": request_id, "status": "PENDING_REVIEW"}
