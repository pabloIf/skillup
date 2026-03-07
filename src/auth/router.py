from fastapi import APIRouter, HTTPException, Depends
from auth.service import hash_password, verify_password, create_access_token
from auth.crud import get_user_by_username, create_user
from fastapi.security import OAuth2PasswordRequestForm
from auth.schemas import UserCreate, UserResponse


auth_router = APIRouter()


@auth_router.post("/register", response_model=UserResponse)
def register(user: UserCreate):
    if get_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed = hash_password(user.password)
    user_obj = create_user(user.username, hashed)

    return {"id": user_obj["id"], "username": user_obj["username"]}

@auth_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    db_user = get_user_by_username(form_data.username)

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not verify_password(form_data.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = create_access_token({"sub": db_user["username"]})

    return {"access_token": token, "token_type": "bearer"}