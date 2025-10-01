from __future__ import annotations
from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    role: str = Field(default="employee")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class LeaveRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    request_id: str = Field(index=True, unique=True)
    user_name: str
    start_date: date
    end_date: date
    status: str = Field(default="PENDING_REVIEW")
    capacity: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    request_id: Optional[str] = Field(default=None, index=True)
    actor: str
    action: str
    details: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
