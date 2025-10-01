from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import chat as chat_router
from app.api.v1 import manager as manager_router
from app.api.v1 import status as status_router
from app.api.v1 import capacity as capacity_router

app = FastAPI(title="Leave Planner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/status/health")
async def health():
    return {"ok": True}

app.include_router(chat_router.router, prefix="/api/v1")
app.include_router(manager_router.router, prefix="/api/v1/manager")
app.include_router(status_router.router, prefix="/api/v1")
app.include_router(capacity_router.router, prefix="/api/v1")

