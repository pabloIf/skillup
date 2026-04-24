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
    
    return calculate_streaks([datetime.strptime(log["log_date"], "%Y-%m-%d").date() for log in logs])

def add_skill(skill: schemas.SkillsCreate, current_user: dict) -> schemas.SkillsResponce:
    skill_data = crud.create_skill(skill.name, current_user["id"])
    return schemas.SkillsResponce(**skill_data)

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
    
    try:
        crud.delete_skill(skill_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"detail": "Skill deleted"}
