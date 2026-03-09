from fastapi import APIRouter, Depends

from auth.dependencies import get_current_user
from skills.schemas import Skills
from . import service


skills_router = APIRouter()

@skills_router.get("/skills")
def get_skills(current_user: dict = Depends(get_current_user)):
    return service.get_skills(user_id=current_user["id"])

@skills_router.get("/skills/{skill_id}")
def get_skill(skill_id: int, current_user: dict = Depends(get_current_user)):
    skill = service.get_skill(skill_id, current_user)
    return skill

@skills_router.get("/skills/{skill_id}/stats")
def get_skill_stats(skill_id: int, current_user: dict = Depends(get_current_user)):
    stats = service.get_skill_stats(skill_id, current_user)
    return stats

@skills_router.post("/skills")
def add_skill(skill: Skills, current_user: dict = Depends(get_current_user)):
    return service.add_skill(skill, current_user)

@skills_router.delete("/skills/{skill_id}")
def remove_skill(skill_id: int, current_user: dict = Depends(get_current_user)):
    return service.remove_skill(skill_id, current_user)