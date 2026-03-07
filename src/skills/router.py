from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from skills.crud import get_skills_by_user, create_skill, delete_skill, get_skill_by_id
from logs.crud import get_logs_by_skill_id, delete_logs_by_skill_id
from stats.service import calculate_streaks
from auth.dependencies import get_current_user
from skills.schemas import Skills


skills_router = APIRouter()


@skills_router.get("/skills")
def get_skills(current_user: dict = Depends(get_current_user)):
    return get_skills_by_user(user_id=current_user["id"])

@skills_router.get("/skills/{skill_id}")
def get_skill(skill_id: int, current_user: dict = Depends(get_current_user)):
    skill = get_skill_by_id(skill_id, current_user["id"])
    if not skill:
        raise HTTPException(status_code=404, detail="skill not found")
    return skill

@skills_router.get("/skills/{skill_id}/stats")
def get_skill_stats(skill_id: int, current_user: dict = Depends(get_current_user)):
    skill = get_skill_by_id(skill_id, current_user["id"])
    if not skill:
        raise HTTPException(status_code=404, detail="skill not found")
    logs = get_logs_by_skill_id(skill_id)
    if not logs:
        return {"detail": "No logs for this skill"}
    return calculate_streaks([datetime.strptime(log["date"], "%Y-%m-%d").date() for log in logs])

@skills_router.post("/skills")
def add_skill(skill: Skills, current_user: dict = Depends(get_current_user)):
    return create_skill(skill.name, current_user["id"])

@skills_router.delete("/skills/{skill_id}")
def remove_skill(skill_id: int, current_user: dict = Depends(get_current_user)):
    skill = get_skill_by_id(skill_id, current_user["id"])
    if not skill:
        raise HTTPException(status_code=404, detail="skill not found") 
    delete_logs_by_skill_id(skill_id)
    delete_skill(skill_id)   
    return { "detail": "Skill deleted" }