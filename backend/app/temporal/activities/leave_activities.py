from temporalio import activity
from app.db.session import get_session
from app.db import crud

@activity.defn
async def update_request_status(request_id: str, status: str, details: str = "") -> bool:
    """Update leave request status in database"""
    try:
        with next(get_session()) as session:
            lr = crud.update_leave_status(session, request_id=request_id, status=status)
            if lr:
                crud.add_audit(session, request_id=request_id, actor="system", action=status, details=details)
                return True
            return False
    except Exception as e:
        activity.logger.error(f"Failed to update status for {request_id}: {e}")
        return False

@activity.defn
async def log_audit_event(request_id: str, actor: str, action: str, details: str = "") -> bool:
    """Log audit event"""
    try:
        with next(get_session()) as session:
            crud.add_audit(session, request_id=request_id, actor=actor, action=action, details=details)
            return True
    except Exception as e:
        activity.logger.error(f"Failed to log audit for {request_id}: {e}")
        return False

@activity.defn
async def send_reminder_notification(request_id: str, manager_name: str = "manager") -> bool:
    """Send reminder notification to manager"""
    try:
        with next(get_session()) as session:
            crud.add_audit(session, request_id=request_id, actor="system", action="REMINDER_SENT", details=f"Notified {manager_name}")
            activity.logger.info(f"Reminder sent for {request_id} to {manager_name}")
            return True
    except Exception as e:
        activity.logger.error(f"Failed to send reminder for {request_id}: {e}")
        return False
