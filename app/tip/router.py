from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from app.config.database import get_db
from app.auth.security import get_current_user
from app.project.repository import receive_project_by_id
from app.user.schemas import UserOut

from .schemas import TipOut, TipSaveIn
from .repository import receive_all_tips, add_many_tips, delete_many_tips

tip_router = APIRouter()


@tip_router.post("/{project_id}")
async def save_tips(project_id: int, tips_list: list[TipSaveIn],
                    current_user: Annotated[UserOut, Depends(get_current_user)],
                    db=Depends(get_db)):
    project = receive_project_by_id(current_user.id, project_id, db)

    if not project:
        raise HTTPException(status_code=400)
    new_tips = []
    old_tips_id = []
    for tip_data in tips_list:
        if tip_data.id is None:
            new_tips.append(tip_data)
            continue
        old_tips_id.append(tip_data.id)

    tips_in_db = receive_all_tips(project.id, db)

    add_many_tips(new_tips, db)

    delete_tips = []
    for tip_in_db in tips_in_db:
        if tip_in_db.id not in old_tips_id:
            delete_tips.append(tip_in_db)
    delete_many_tips(delete_tips, db)

    return receive_all_tips(project.id, db)


@tip_router.get("/{project_id}", response_model=list[TipOut])
async def get_tips(project_id: int, current_user: Annotated[UserOut, Depends(get_current_user)],
                   db=Depends(get_db)):
    project = receive_project_by_id(current_user.id, project_id, db)

    if not project:
        raise HTTPException(status_code=400)

    return receive_all_tips(project.id, db)
