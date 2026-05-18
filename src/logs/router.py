from fastapi import APIRouter, Depends
from auth.dependencies import get_current_user
from logs.schemas import Log
from . import service

from database import get_connection
from uow.unit_of_work import UnitOfWork


logs_router = APIRouter(tags=["Logs"])

@logs_router.get("/logs/skill/{skill_id}")
def get_logs_for_skill(skill_id: int, current_user: dict = Depends(get_current_user)):
    logs = service.get_logs_for_skill(skill_id, current_user)
    return logs

@logs_router.post("/logs")
def create_log(log: Log, current_user: dict = Depends(get_current_user)):
    with get_connection() as conn:
        with UnitOfWork(conn) as uow:
            return service.create_log(uow, log, current_user)

@logs_router.delete("/logs")
def remove_log(log_id: int, current_user: dict = Depends(get_current_user)):
    service.delete_log(log_id, current_user)
    return { "detail": "Log deleted"}