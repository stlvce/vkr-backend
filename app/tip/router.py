from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from app.config.database import get_db
from app.auth.security import get_current_user
from app.project.repository import receive_project_by_id
from app.user.schemas import UserOut

from .schemas import TipOut
from .repository import receive_all_tips

tip_router = APIRouter()


@tip_router.get("/{project_id}", response_model=list[TipOut])
async def get_tips(project_id: int, current_user: Annotated[UserOut, Depends(get_current_user)],
                   db=Depends(get_db)):
    project = receive_project_by_id(current_user.id, project_id, db)

    if not project:
        raise HTTPException(status_code=400)

    return receive_all_tips(project.id, db)
