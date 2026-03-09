import os
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from dotenv import load_dotenv

from . import crud
from . import schemas

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
    
    hashed = hash_password(user.password)
    user_obj = crud.create_user(user.username, hashed)

    return user_obj

def login(form_data: OAuth2PasswordRequestForm) -> dict:
    db_user = crud.get_user_by_username(form_data.username)

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not verify_password(form_data.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = create_access_token({"sub": str(db_user["id"])})

    return {"access_token": token, "token_type": "bearer"}