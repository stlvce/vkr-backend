from fastapi import APIRouter, Depends, HTTPException, Response, Form
from typing import Annotated

from app.config.database import get_db
from app.auth.security import get_current_user
from app.user.schemas import UserOut
from app.project.repository import project_repository

from .repository import neighbor_repository
from .schemas import NeighborIn, NeighborOut, NeighborDelete, LocationEnum

neighbor_router = APIRouter()


@neighbor_router.post("")
async def create_neighbor(neighbor_data: NeighborIn,
                          current_user: Annotated[UserOut, Depends(get_current_user)],
                          db=Depends(get_db)):
    project = project_repository.get(neighbor_data.project_id, db)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=400)

    neighbor_repository.create(neighbor_data, db)

    return Response(status_code=200)

@neighbor_router.post("/{project_id}")
async def update_neighbours(project_id: int, locations: list[LocationEnum], current_user: Annotated[UserOut, Depends(get_current_user)],
                          db=Depends(get_db)):
    project = project_repository.get(project_id, db)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=400)
    
    for location in locations:
        if location in project.land.red_borders:
            raise HTTPException(status_code=400, detail="Участок соседа пересекается с красной линией улицы")

    neighbours_db = neighbor_repository.get_all_by_project_id(project_id, db)

    deletion_neighbours = []
    addition_neighbours = locations

    for neighbor in neighbours_db:
        if neighbor.location not in locations:
            deletion_neighbours.append(neighbor)
        else:
            location_index = locations.index(neighbor.location)
            addition_neighbours.pop(location_index)

    if len(addition_neighbours) != 0:
        neighbor_repository.create_multi(project_id, addition_neighbours, db)

    if len(deletion_neighbours) != 0:
        neighbor_repository.delete_multi(deletion_neighbours, db)

    return Response(status_code=200)


@neighbor_router.delete("")
async def delete_neighbor(neighbor_data: NeighborDelete,
                          current_user: Annotated[UserOut, Depends(get_current_user)],
                          db=Depends(get_db)):
    project = project_repository.get(neighbor_data.project_id, db)

    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=400)

    neighbor_repository.delete(neighbor_data.id, db)

    return Response(status_code=200)
