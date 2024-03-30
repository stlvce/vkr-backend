from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import engine
from app.config.models import Base
from app.user.router import user_router
from app.auth.router import auth_router
from app.project.router import project_router
from app.expert.router import expert_router
from app.rule.router import rule_router
from app.building.router import building_router
from app.tip.router import tip_router

app = FastAPI(docs_url="/api/docs")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(project_router)
app.include_router(building_router)
# app.include_router(tip_router)
app.include_router(expert_router)
app.include_router(rule_router)
