from pydantic import BaseModel

class Skills(BaseModel):
    user_id: int
    name: str