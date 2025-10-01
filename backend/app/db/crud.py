from datetime import datetime
from typing import Optional
from sqlmodel import Session, select
from .models import LeaveRequest, AuditLog


def create_leave_request(session: Session, *, request_id: str, user_name: str, start_date, end_date, capacity: Optional[str]) -> LeaveRequest:
    lr = LeaveRequest(
        request_id=request_id,
        user_name=user_name,
        start_date=start_date,
        end_date=end_date,
        status="PENDING_REVIEW",
        capacity=capacity,
    )
    session.add(lr)
    session.commit()
    session.refresh(lr)
    return lr


def update_leave_status(session: Session, *, request_id: str, status: str) -> Optional[LeaveRequest]:
    lr = session.exec(select(LeaveRequest).where(LeaveRequest.request_id == request_id)).first()
    if not lr:
        return None
    lr.status = status
    lr.updated_at = datetime.utcnow()
    session.add(lr)
    session.commit()
    session.refresh(lr)
    return lr


def get_leave_by_request_id(session: Session, *, request_id: str) -> Optional[LeaveRequest]:
    return session.exec(select(LeaveRequest).where(LeaveRequest.request_id == request_id)).first()


def list_pending_requests(session: Session):
    return session.exec(select(LeaveRequest).where(LeaveRequest.status == "PENDING_REVIEW")).all()


def add_audit(session: Session, *, request_id: Optional[str], actor: str, action: str, details: Optional[str] = None) -> AuditLog:
    log = AuditLog(request_id=request_id, actor=actor, action=action, details=details)
    session.add(log)
    session.commit()
    session.refresh(log)
    return log
