from sqlalchemy.orm import Session

from app.config.models import InitBuildingModel

from .schemas import InitBuildingCreate, InitBuildingOut


def add_new_init_building(init_building_data: InitBuildingCreate, db: Session) -> InitBuildingOut:
    new_init_building = InitBuildingModel(**init_building_data.dict())
    db.add(new_init_building)
    db.commit()
    db.refresh(new_init_building)
    return new_init_building


def receive_init_buildings(db: Session) -> list[InitBuildingOut]:
    return db.query(InitBuildingModel).all()


def receive_init_buildings_by_type_id(type_permission_id: int, db: Session) -> list[InitBuildingOut]:
    return db.query(InitBuildingModel).filter(InitBuildingModel.type_permission_id == type_permission_id).all()
