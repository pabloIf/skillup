from fastapi import APIRouter, HTTPException, Depends
from logs.crud import get_log_by_id, get_logs_by_skill_id, create_log, delete_log, delete_logs_by_skill_id
from skills.crud import get_skill_by_id
from auth.dependencies import get_current_user
from logs.schemas import Log

logs_router = APIRouter()


@logs_router.get("/logs/skill/{skill_id}")
def logs_for_skill(skill_id: int, current_user: dict = Depends(get_current_user)):
    skill = get_skill_by_id(skill_id, current_user["id"])
    if not skill:
        raise HTTPException(status_code=404, detail="Logs not found")

    logs = get_logs_by_skill_id(skill_id)
    if not logs:
        return {"detail": "No logs for this skill"}
    return logs

@logs_router.post("/logs")
def add_log(log: Log, current_user: dict = Depends(get_current_user)):
    skill = get_skill_by_id(log.skill_id, current_user["id"])
    if not skill:
        raise HTTPException(status_code=404, detail="skill not found")
    
    if skill["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    return create_log(skill_id=skill["id"], log_date=log.date)

@logs_router.delete("/logs")
def remove_log(log_id: int, current_user: dict = Depends(get_current_user)):
    log = get_log_by_id(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="log not found")
    
    skill = get_skill_by_id(log["skill_id"], current_user["id"])
    if not skill:
        raise HTTPException(status_code=404, detail="skill not found")
    delete_log(log_id)
    return { "detail": "Log deleted"}