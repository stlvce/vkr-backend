from sqlalchemy.orm import Session

from .model import ProjectModel
from .schemas import ProjectCreate


def add_new_project(user_id: int, project_data: ProjectCreate, db: Session):
    new_project = ProjectModel(user_id=user_id, **project_data.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project
