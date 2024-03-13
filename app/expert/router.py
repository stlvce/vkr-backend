from fastapi import APIRouter, HTTPException, Depends
from app.database import get_db, engine, Base

expert_router = APIRouter(prefix="/expert", tags=["Expert"])

Base.metadata.create_all(bind=engine)


@expert_router.post("/calculate")
async def calculate_distance(body):
    pass
