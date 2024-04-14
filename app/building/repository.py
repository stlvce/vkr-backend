from sqlalchemy.orm import Session

from app.config.models import BuildingModel

from .schemas import BuildingIn, BuildingOut


def add_new_building(building_data: BuildingIn, db: Session) -> BuildingOut:
    new_building = BuildingModel(**building_data.dict())
    db.add(new_building)
    db.commit()
    db.refresh(new_building)
    return new_building


def receive_buildings(project_id: int, db: Session):
    buildings = db.query(BuildingModel).filter(BuildingModel.project_id == project_id).all()

    return buildings
