from sqlalchemy.orm import Session

from app.config.models import InitBuildingModel
from app.config.repository_base import RepositoryBase

from .schemas import InitBuildingIn


class InitBuildingRepository(RepositoryBase[InitBuildingModel, InitBuildingIn, InitBuildingIn]):
    def get_by_type_permission(self, type_permission_id: int, db: Session):
       return db.query(self.model).filter(self.model.type_permission_id == type_permission_id).all()


init_building_repository = InitBuildingRepository(InitBuildingModel)