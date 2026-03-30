from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from auth.service import decode_token
from auth.crud import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    user_id = decode_token(token)
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user