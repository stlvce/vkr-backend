from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import engine
from app.config.models import Base
from app.user.router import user_router
from app.auth.router import auth_router
from app.project.router import project_router
from app.land.router import land_router
from app.building.router import building_router
from app.tip.router import tip_router
from app.expert.router import expert_router
from app.norm.router import norm_router
from app.land_category.router import land_category_router
from app.type_permission.router import type_permission_router
from app.init_buildings.router import init_building_router
from app.documents.router import document_router
from app.material.router import material_router
from app.neighbours.router import neighbor_router

app = FastAPI(docs_url="/api/docs", version="1.0.0", openapi_url="/api/openapi.json",
              swagger_ui_parameters={"operationsSorter": "method", "syntaxHighlight.theme": "obsidian"})

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(user_router, prefix="/api/user", tags=["user"])
app.include_router(project_router, prefix="/api/project", tags=["project"])
app.include_router(neighbor_router, prefix="/api/neighbor", tags=["neighbor"])
app.include_router(land_router, prefix="/api/land", tags=["land"])
app.include_router(building_router, prefix="/api/building", tags=["building"])

app.include_router(tip_router, prefix="/api/tip", tags=["tip"])
app.include_router(expert_router, prefix="/api/expert", tags=["expert"])

app.include_router(land_category_router, prefix="/api/land-category", tags=["land category"])
app.include_router(type_permission_router, prefix="/api/type-permission", tags=["type permission"])
app.include_router(init_building_router, prefix="/api/init-building", tags=["init building"])
app.include_router(norm_router, prefix="/api/norm", tags=["norm"])
app.include_router(document_router, prefix="/api/document", tags=["document"])
app.include_router(material_router, prefix="/api/material", tags=["material"])
