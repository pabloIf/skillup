from pydantic import BaseModel
from datetime import date

class Log(BaseModel):
    skill_id: int
    date: date