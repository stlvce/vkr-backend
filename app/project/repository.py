from sqlalchemy.orm import Session
from .model import ProjectModel
from .schemas import ProjectCreate


def add_new_project(project_data: ProjectCreate, db: Session):
    new_project = ProjectModel(user_id=1, neighbors_location=project_data.neighbors_location,
                               width_parcel=project_data.width_parcel,
                               length_parcel=project_data.length_parcel)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project
