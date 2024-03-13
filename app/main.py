from fastapi import FastAPI
from app.user.router import user_router
from app.auth.router import auth_router
from app.project.router import project_router
from app.expert.router import expert_router
from app.rule.router import rule_router

app = FastAPI(swagger_ui_parameters={"tokenUrl": "/auth/login"})

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(project_router)
app.include_router(expert_router)
app.include_router(rule_router)
