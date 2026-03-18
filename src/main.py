from fastapi import FastAPI
from database import init_db
from auth.router import auth_router
from logs.router import logs_router
from skills.router import skills_router

app = FastAPI()

init_db()

app.include_router(skills_router, prefix="/api")
app.include_router(logs_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
