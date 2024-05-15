from sqlalchemy.orm import Session, joinedload

from app.config.models import BuildingModel
from app.project.repository import receive_project_by_id

from .schemas import BuildingCreate, BuildingOut, BuildingEdit


def add_new_building(building_data: BuildingCreate, db: Session) -> BuildingOut:
    new_building = BuildingModel(**building_data.dict())
    db.add(new_building)
    db.commit()


def add_many_buildings(building_list: list[BuildingCreate], db: Session):
    commit_list = []
    for item in building_list:
        commit_list.append(BuildingModel(**item.dict()))
    db.add_all(commit_list)
    db.commit()


def receive_buildings(project_id: int, db: Session):
    buildings = db.query(BuildingModel).where(BuildingModel.project_id == project_id).options(
        joinedload(BuildingModel.material)).all()

    return buildings


def change_building_info(building_id: int, new_building_info: BuildingEdit, db: Session) -> BuildingOut | None:
    building = db.get(BuildingModel, building_id)
    if not building:
        return None
    setattr(building, "material_id", new_building_info.material_id)
    setattr(building, "title", new_building_info.title)
    setattr(building, "start_x", new_building_info.start_x)
    setattr(building, "start_y", new_building_info.start_y)
    setattr(building, "width", new_building_info.width)
    setattr(building, "length", new_building_info.length)
    setattr(building, "height", new_building_info.height)

    db.commit()
    db.refresh(building)
    return building


def remove_building_by_id(user_id: int, project_id: int, building_id: int, db: Session) -> bool:
    project = receive_project_by_id(user_id, project_id, db)
    if not project:
        return False

    building = db.get(BuildingModel, building_id)
    if not building:
        return False

    db.delete(building)
    db.commit()
    return True
