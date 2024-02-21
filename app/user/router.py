from fastapi import APIRouter, HTTPException, Depends
from .repository import add_new_user
from .schemas import UserCreate
from app.database import get_db, engine, Base

user_router = APIRouter(prefix="/api/user", tags=["User"])

Base.metadata.create_all(bind=engine)


@user_router.get("/info")
async def get_user_info():
    return "Receive user info"


# TODO перенести в регистрацию
@user_router.post("/create")
async def create_user(user: UserCreate, db=Depends(get_db)):
    new_user = add_new_user(user, db)
    if not new_user:
        raise HTTPException(status_code=400, detail="NOT_UNIQ_EMAIL_OR_USERNAME")
    return None


@user_router.put("/edit")
async def edit_user(new_user_info):
    return "Edit user info"


@user_router.delete("/delete")
async def delete_user():
    return "Delete user"
