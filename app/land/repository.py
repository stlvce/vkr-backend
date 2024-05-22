from sqlalchemy.orm import Session

from app.config.repository_base import RepositoryBase
from app.config.models import LandModel
from app.project.repository import project_repository

from .schemas import LandIn, LandOut, LandEdit, LandCreate


class LandRepository(RepositoryBase[LandModel, LandCreate, LandEdit]):
    def get_by_project_id(self, project_id: int, db: Session) -> LandOut | None:
        return db.query(self.model).where(self.model.project_id == project_id).first()
    
    def get_all_by_type_permission_id(self, typ_permission_id: int, db: Session) -> LandOut | None:
        return db.query(self.model).where(self.model.type_permission_id == typ_permission_id).all()

land_repository = LandRepository(LandModel)