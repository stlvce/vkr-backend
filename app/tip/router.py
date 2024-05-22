from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Annotated

from app.config.database import get_db
from app.auth.security import get_current_user
from app.project.repository import project_repository
from app.user.schemas import UserOut

from .schemas import TipOut, TipSaveIn
from .repository import tip_repository

tip_router = APIRouter()


@tip_router.post("/{project_id}")
async def save_tips(project_id: int, tips_list: list[TipSaveIn],
                    current_user: Annotated[UserOut, Depends(get_current_user)],
                    db=Depends(get_db)):
    project = project_repository.get(project_id, db)

    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=400)
    new_tips = []
    old_tips_id = []
    for tip_data in tips_list:
        if tip_data.id is None:
            new_tips.append(tip_data)
            continue
        old_tips_id.append(tip_data.id)

    tips_in_db = tip_repository.get_all(project.id, db)

    tip_repository.create_multi(new_tips, db)

    delete_tips = []
    for tip_in_db in tips_in_db:
        if tip_in_db.id not in old_tips_id:
            delete_tips.append(tip_in_db)
    tip_repository.delete_multi(delete_tips, db)

    return Response(status_code=200)


@tip_router.get("/{project_id}", response_model=list[TipOut])
async def get_tips(project_id: int, current_user: Annotated[UserOut, Depends(get_current_user)],
                   db=Depends(get_db)):
    project = project_repository.get(project_id, db)

    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=400)

    return tip_repository.get_all(project.id, db)
