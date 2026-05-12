from fastapi import Depends, HTTPException
from datetime import date, timedelta
import sqlite3

from auth.dependencies import get_current_user
from skills.crud import get_skill_by_id, update_skill
from stats.service import calculate_streak
from . import crud
from . import schemas



def create_log(log: schemas.Log, current_user: dict) -> dict:
    skill = get_skill_by_id(log.skill_id, current_user["id"])
    if not skill:
        raise HTTPException(status_code=404, detail="skill not found")
        
    result_streak = calculate_streak(skill=skill, today=log.date)
    if result_streak is None:
        raise HTTPException(status_code=400, detail="Already checked in")
        
    xp = skill["xp"] + 1 #calculate %
    
    try:
        created_log = crud.create_log(skill_id=skill["id"], log_date=log.date)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Already checked in")

    update_skill(skill["id"], {
        "current_streak": result_streak["current_streak"],
        "max_streak": result_streak["max_streak"],
        "last_log_date": log.date,
        "xp": xp
    })
    return created_log

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