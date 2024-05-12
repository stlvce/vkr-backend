from fastapi import APIRouter, Depends, HTTPException, Response, Form
from typing import Annotated

from app.config.database import get_db
from app.auth.security import get_current_user
from app.user.schemas import UserOut
from app.project.repository import receive_project_by_id

from .repository import neighbor_repository
from .schemas import NeighborIn, NeighborOut, NeighborDelete

neighbor_router = APIRouter()


@neighbor_router.post("")
async def create_neighbor(neighbor_data: NeighborIn,
                          current_user: Annotated[UserOut, Depends(get_current_user)],
                          db=Depends(get_db)):
    project = receive_project_by_id(current_user.id, neighbor_data.project_id, db)
    if not project:
        raise HTTPException(status_code=400)

    neighbor_repository.create(neighbor_data, db)

    return Response(status_code=200)


@neighbor_router.delete("")
async def delete_neighbor(neighbor_data: NeighborDelete,
                          current_user: Annotated[UserOut, Depends(get_current_user)],
                          db=Depends(get_db)):
    project = receive_project_by_id(current_user.id, neighbor_data.project_id, db)

    if not project:
        raise HTTPException(status_code=400)

    neighbor_repository.delete(neighbor_data.id, db)

    return Response(status_code=200)
