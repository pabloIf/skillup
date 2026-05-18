from pydantic import BaseModel, field_validator
from typing import Optional

class Skills(BaseModel):
    user_id: int
    name: str

class SkillsCreate(BaseModel):
    name: str

    @field_validator("name")
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v
    
class SkillsResponce(BaseModel):
    id: int
    name: str

class SkillsPatch(BaseModel):
    name: Optional[str] = None