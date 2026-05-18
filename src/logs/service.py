from fastapi import Depends, HTTPException
from sqlite3 import IntegrityError

from auth.dependencies import get_current_user
from skills.crud import get_skill_by_id
from stats.service import calculate_streak, calculate_xp
from uow.unit_of_work import UnitOfWork
from . import crud
from . import schemas



def create_log(uow: UnitOfWork, log: schemas.Log, current_user: dict) -> dict:
    skill = uow.skills.get_by_id(log.skill_id, current_user["id"])
    if not skill:
        raise HTTPException(status_code=404, detail="skill not found")
    
    try:
        streak = calculate_streak(skill=skill, today=log.date)
        xp = calculate_xp(skill_xp=skill["xp"])

        uow.logs.create(skill_id=skill["id"], log_date=log.date)
        uow.skills.update(skill["id"], {
            "current_streak": streak["current_streak"],
            "max_streak": streak["max_streak"],
            "last_log_date": log.date,
            "xp": xp
            })
        
        return {"status": "ok"}
    except IntegrityError:
        raise HTTPException(status_code=409, detail="already exists")


def delete_log(log_id: int, current_user: dict) -> dict:
    log = crud.get_log_by_id(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="log not found")
    
    skill = get_skill_by_id(log["skill_id"], current_user["id"])
    if not skill:
        raise HTTPException(status_code=404, detail="skill not found")
    crud.delete_log(log_id)
    return { "detail": "Log deleted"}

def get_logs_for_skill(skill_id: int, current_user: dict = Depends(get_current_user)):
    skill = get_skill_by_id(skill_id, current_user["id"])
    if not skill:
        raise HTTPException(status_code=404, detail="Logs not found")

    logs = crud.get_logs_by_skill_id(skill_id)
    if not logs:
        return {"detail": "No logs for this skill"}
    return logs