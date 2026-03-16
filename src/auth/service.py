import os
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from dotenv import load_dotenv

from . import crud
from . import schemas
from . import utils

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password):
    return pwd_context.verify(password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")
    

def register(user: schemas.UserCreate) -> dict:
    if crud.get_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="User already exists")
    if crud.get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    hashed = hash_password(user.password)
    user_obj = crud.create_user(user.username, hashed, user.email)

    return {
        "id": user_obj["user_id"],
        "username": user_obj["username"]
    }

def login(form_data: OAuth2PasswordRequestForm) -> dict:
    db_user = crud.get_user_by_username(form_data.username)

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not crud.is_active(db_user["id"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not verify_password(form_data.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = create_access_token({"sub": str(db_user["id"])})

    return {"access_token": token, "token_type": "bearer"}



def create_reactivate_token(user_id: int):
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode = {"sub": str(user_id), "exp": expire}
    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return token

def deactivate_user(current_user):
    return crud.deactivate_user(current_user["id"])

def request_reactivate(email: str):
    user = crud.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    if user["is_active"]:
        raise HTTPException(status_code=400, detail="User is already active")
    
    token = create_reactivate_token(user["id"])
    utils.send_reactivate_email(user["email"], token)

    return {"detail": "email has been send"}

def reactivate_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expire token")
    
    crud.reactivate_user(user_id)
    return {"detail": "User reactivated, you can close this page"}


def get_all_users():
    return crud.get_all_users()

def delete_user(user_id: int):
    user = crud.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(user_id)

    return {"detail": "User deleted"}