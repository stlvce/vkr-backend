from fastapi import FastAPI
from app.user.router import user_router
from app.auth.router import auth_router
from app.project.router import project_router
from app.expert.router import expert_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(project_router)
app.include_router(expert_router)
