from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .schemas import UserResponse, UserCreate
from . import service
from .dependencies import get_current_user


auth_router = APIRouter()

@auth_router.post("/register", response_model=UserResponse)
def register(user: UserCreate):
    return service.register(user)

@auth_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return service.login(form_data)