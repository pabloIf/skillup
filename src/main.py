from fastapi import FastAPI
from database import init_db
from auth.router import auth_router
from logs.router import logs_router
from skills.router import skills_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "http://127.0.0.1:8000",
    "http://localhost:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(skills_router, prefix="/api")
app.include_router(logs_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
