from sqlalchemy.orm import Session, joinedload

from app.config.repository_base import RepositoryBase
from app.config.models import BuildingModel

from .schemas import BuildingCreate, BuildingOut, BuildingEdit

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

building_repository = BuildingRepository(BuildingModel)
