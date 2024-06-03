from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, joinedload

from app.config.repository_base import RepositoryBase
from app.config.models import BuildingModel

from .schemas import BuildingCreate, BuildingOut, BuildingEdit, BuildingSaveIn

class BuildingRepository(RepositoryBase[BuildingModel, BuildingCreate, BuildingEdit]):
    def create_multi(self, building_list: list[BuildingCreate], db):
        commit_list = []
        for item in building_list:
            commit_list.append(BuildingModel(**item.dict()))
        db.add_all(commit_list)
        db.commit()

    def get_all(self, project_id: int, db: Session) -> list[BuildingOut]:
        buildings = db.query(self.model).where(self.model.project_id == project_id).options(
        joinedload(self.model.material)).all()

        return buildings

    def multi_update(self, project_id: int, buildings_list: list[BuildingSaveIn], db: Session):
        db_buildings = self.get_all(project_id, db)

        for obj_in in buildings_list:
            db_obj = [item for item in db_buildings if item.id == obj_in.id][0]
            obj_data = jsonable_encoder(db_obj)
            update_data = obj_in.dict()

            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])

        db.commit()

building_repository = BuildingRepository(BuildingModel)
