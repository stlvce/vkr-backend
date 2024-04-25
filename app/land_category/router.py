from fastapi import APIRouter, Depends, HTTPException, Response

from app.config.database import get_db
from app.auth.security import get_current_admin

from .repository import land_category_repository
from .schemas import LandCategoryIn, LandCategoryOut

land_category_router = APIRouter()


@land_category_router.post("", dependencies=[Depends(get_current_admin)])
async def create_land_category(land_category_data: LandCategoryIn, db=Depends(get_db)):
    land_category_repository.create(land_category_data, db)
    return Response(status_code=200)


@land_category_router.get("", response_model=list[LandCategoryOut])
async def get_all_land_categories(db=Depends(get_db)):
    return land_category_repository.get_all(db)


@land_category_router.get("/{land_category_id}", response_model=LandCategoryOut)
async def get_land_category_by_id(land_category_id: int, db=Depends(get_db)):
    land_category = land_category_repository.get(land_category_id, db)

    if not land_category:
        raise HTTPException(status_code=400)

    return land_category


@land_category_router.put("/{land_category_id}", dependencies=[Depends(get_current_admin)])
async def update_land_category(land_category_id: int, land_category_data: LandCategoryIn, db=Depends(get_db)):
    land_category = land_category_repository.update(land_category_id, land_category_data, db)

    if not land_category:
        raise HTTPException(status_code=400)

    return Response(status_code=200)


@land_category_router.delete("/{land_category_id}", dependencies=[Depends(get_current_admin)])
async def delete_land_category(land_category_id: int, db=Depends(get_db)):
    deleted_land_category = land_category_repository.delete(land_category_id, db)

    if not deleted_land_category:
        raise HTTPException(status_code=400)

    return Response(status_code=200)
