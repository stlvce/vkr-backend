from sqlalchemy.orm import Session

from app.config.models import LandModel
from app.project.repository import receive_project_by_id

from .schemas import LandIn, LandOut, LandEdit


def create_land(project_id: int, new_land: LandIn, db: Session):
    land = LandModel(project_id=project_id, **new_land.dict())
    db.add(land)
    db.commit()


def read_land_by_project_id(user_id, project_id, db: Session) -> LandOut | None:
    project = receive_project_by_id(user_id, project_id, db)

    if not project:
        return None

    return db.query(LandModel).filter(LandModel.project_id == project_id).first()


def read_land_by_type_permission_id(typ_permission_id: int, db: Session) -> list[LandOut]:
    return db.query(LandModel).where(LandModel.type_permission_id == typ_permission_id).all()


def update_land_by_project_id(user_id: int, project_id: int, land_data: LandEdit, db: Session) -> LandOut | None:
    project = receive_project_by_id(user_id, project_id, db)

    if not project:
        return None

    land = db.query(LandModel).filter(LandModel.project_id == project_id).first()

    setattr(land, "land_category_id", land_data.land_category_id)
    setattr(land, "type_permission_id", land_data.type_permission_id)
    setattr(land, "width_parcel", land_data.width_parcel)
    setattr(land, "length_parcel", land_data.length_parcel)
    setattr(land, "red_borders", land_data.red_borders)

    db.commit()
    
    return land
