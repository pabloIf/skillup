from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .schemas import UserResponse, UserCreate
from . import service
from .dependencies import get_current_user


auth_router = APIRouter(tags=["Auth"])

@auth_router.post("/register", response_model=UserResponse)
def register(user: UserCreate):
    return service.register(user)

@auth_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return service.login(form_data)

@auth_router.post("/users/deactivate")
def deactivate_user(current_user = Depends(get_current_user)):
    return service.deactivate_user(current_user)

@auth_router.post("/users/request-reactivate")
def request_reactivate(email: str):
    return service.request_reactivate(email)

@auth_router.get("/users/reactivate")
def reactivate_user(token: str):
    return service.reactivate_user(token)

@auth_router.get("/users")
def get_all_users():
    return service.get_all_users()

@auth_router.delete("/users/{user_id}")
def delete_user(user_id: int):
    return service.delete_user(user_id)