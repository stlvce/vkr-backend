from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .repository import add_new_user
from .schemas import UserCreate
from app.database import engine, Base, SessionLocal

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


userRouter = APIRouter(prefix="/api/user", tags=["items"])


@userRouter.post("/create")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    add_new_user(db, user)
