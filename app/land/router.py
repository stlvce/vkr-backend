from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Annotated

from app.config.database import get_db
from app.user.schemas import UserOut
from app.auth.security import get_current_user
from app.project.repository import project_repository

from .schemas import LandOut, LandEdit
from .repository import land_repository

land_router = APIRouter()


@land_router.get("/{project_id}", response_model=LandOut)
async def get_land_by_project_id(project_id: int, current_user: Annotated[UserOut, Depends(get_current_user)],
                                 db=Depends(get_db)):
    project = project_repository.get(project_id, db)

    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=400)

    land = land_repository.get_by_project_id(project_id, db)

    if not land:
        raise HTTPException(status_code=400)

    return land


@land_router.put("/{project_id}")
async def change_land_info(project_id: int, land_data: LandEdit,
                           current_user: Annotated[UserOut, Depends(get_current_user)], db=Depends(get_db)):
    project = project_repository.get(project_id, db)

    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=400)
        
    land = land_repository.update(project.land.id, land_data, db)

    if not land:
        raise HTTPException(status_code=400)

    return Response(status_code=200)
