from pydantic import BaseModel
from typing import Optional

class Skills(BaseModel):
    user_id: int
    name: str

class SkillsPatch(BaseModel):
    name: Optional[str]