from fastapi import HTTPException
from datetime import datetime

from . import crud, schemas
from logs.crud import get_logs_by_skill_id
from stats.service import calculate_streaks

def get_skills(user_id) -> list[dict]:
    return crud.get_skills_by_user_id(user_id)

def get_skill(skill_id: int, current_user: dict) -> dict:
    skill = crud.get_skill_by_id(skill_id, current_user["id"])
    if not skill:
        raise HTTPException(status_code=404, detail="skill not found")
    return skill

def get_skill_stats(skill_id: int, current_user: dict) -> dict:
    skill = crud.get_skill_by_id(skill_id, current_user["id"])
    if not skill:
        raise HTTPException(status_code=404, detail="skill not found")
    logs = get_logs_by_skill_id(skill_id)
    if not logs:
        return {"detail": "No logs for this skill"}
    return calculate_streaks([datetime.strptime(log["date"], "%Y-%m-%d").date() for log in logs])

def add_skill(skill: schemas.Skills, current_user: dict) -> dict:
    return crud.create_skill(skill.name, current_user["id"])

def patch_skill(skill_id: int, skill: schemas.SkillsPatch, current_user: dict):
    db_skill = crud.get_skill_by_id(skill_id, current_user["id"])
    if not db_skill:
        raise HTTPException(status_code=404, detail="skill not found")
    update_data = skill.dict(exclude_unset=True)
    crud.update_skill(skill_id, update_data)
    return {"detail": "SKill Updated"}

def remove_skill(skill_id: int, current_user: dict) -> dict:
    skill = crud.get_skill_by_id(skill_id, current_user["id"])
    if not skill:
        raise HTTPException(status_code=404, detail="skill not found") 
    crud.delete_skill(skill_id)
    return {"detail": "Skill deleted"}
