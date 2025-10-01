from fastapi import APIRouter

router = APIRouter()

@router.get('/capacity')
async def capacity(date: str, role: str | None = None):
    # naive demo rule: weekends red, else yellow
    import datetime
    d = datetime.date.fromisoformat(date)
    level = 'red' if d.weekday() >= 5 else 'yellow'
    return {"date": date, "role": role, "capacity": level}
