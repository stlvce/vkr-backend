from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.config.repository_base import RepositoryBase
from app.config.models import ProjectModel

from .schemas import ProjectIn, ProjectOut, ProjectEdit, ProjectWNeighboursOut, ProjectCreate


class ProjectRepository(RepositoryBase[ProjectModel, ProjectCreate, ProjectEdit]):
    def get_all(self, user_id: int, db: Session, skip: int = 0, limit: int = 100, sort_query: str = "id asc") -> list[ProjectOut]:
        q = select(self.model).where(self.model.user_id == user_id).offset(skip).limit(limit).order_by(text(sort_query))
        result = db.execute(q)
        curr = list(result.scalars())

        return curr

project_repository = ProjectRepository(ProjectModel)
