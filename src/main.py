from fastapi import FastAPI
from database import init_db
from auth.router import auth_router
from logs.router import logs_router
from skills.router import skills_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(skills_router, prefix="/api")
app.include_router(logs_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
