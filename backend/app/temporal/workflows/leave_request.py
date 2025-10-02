from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, List
from temporalio import workflow
from app.temporal.activities.leave_activities import update_request_status, log_audit_event, send_reminder_notification

@dataclass
class LeaveInput:
    request_id: str
    user_name: str
    start_date: str
    end_date: str

@workflow.defn
class LeaveRequestWorkflow:
    def __init__(self) -> None:
        self.request_id: str = ""
        self.status: str = "PENDING_REVIEW"
        self.timeline: List[str] = []

    @workflow.run
    async def run(self, inp: LeaveInput) -> str:
        self.request_id = inp.request_id
        self.status = "PENDING_REVIEW"
        self.timeline = ["created"]

        # Reminder at ~48s
        await workflow.sleep(48)
        if self.status == "PENDING_REVIEW":
            await workflow.execute_activity(
                send_reminder_notification,
                self.request_id,
                schedule_to_close_timeout=workflow.timedelta(seconds=10)
            )
            self.timeline.append("reminder_sent")

        # Auto-release at ~72s (24s after reminder)
        await workflow.sleep(24)
        if self.status == "PENDING_REVIEW":
            await workflow.execute_activity(
                update_request_status,
                self.request_id,
                "AUTO_RELEASED",
                "Auto-released after 72s timeout",
                schedule_to_close_timeout=workflow.timedelta(seconds=10)
            )
            self.status = "AUTO_RELEASED"
            self.timeline.append("auto_released")
        return self.status

    @workflow.signal
    async def manager_decision(self, decision: Literal['APPROVE', 'REJECT']) -> None:
        self.status = 'APPROVED' if decision == 'APPROVE' else 'REJECTED'
        self.timeline.append(f"manager_{decision.lower()}")

    @workflow.signal
    async def employee_cancel(self) -> None:
        self.status = 'CANCELLED'
        self.timeline.append('employee_cancel')

    @workflow.query
    def get_status(self) -> str:
        return self.status

    @workflow.query
    def get_timeline(self) -> List[str]:
        return list(self.timeline)
