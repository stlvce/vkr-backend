from sqlalchemy.orm import Session

from app.config.models import BuildingModel
from app.project.repository import receive_project_by_id

from .schemas import BuildingIn, BuildingOut, BuildingEdit


def add_new_building(building_data: BuildingIn, db: Session) -> BuildingOut:
    new_building = BuildingModel(**building_data.dict())
    db.add(new_building)
    db.commit()
    db.refresh(new_building)
    return new_building


def receive_buildings(project_id: int, db: Session):
    buildings = db.query(BuildingModel).filter(BuildingModel.project_id == project_id).all()

    return buildings


def change_building_info(new_building_info: BuildingEdit, db: Session) -> BuildingOut | None:
    building = db.query(BuildingModel).filter(BuildingModel.id == new_building_info.id).first()
    if not building:
        return None
    setattr(building, "title", new_building_info.title)
    setattr(building, "start_x", new_building_info.start_x)
    setattr(building, "start_y", new_building_info.start_y)
    setattr(building, "width", new_building_info.width)
    setattr(building, "length", new_building_info.length)

    db.commit()
    db.refresh(building)
    return building


def remove_building_by_id(user_id: int, project_id: int, building_id: int, db: Session) -> bool:
    project = receive_project_by_id(user_id, project_id, db)
    if not project:
        return False

    building = db.query(BuildingModel).filter(BuildingModel.id == building_id).first()
    if not building:
        return False

    db.delete(building)
    db.commit()
    return True
