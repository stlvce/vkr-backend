from sqlalchemy.orm import Session
from typing import List

from .model import ProjectModel
from .schemas import ProjectIn, ProjectOut, ProjectEdit


def add_new_project(user_id: int, project_data: ProjectIn, db: Session) -> ProjectOut:
    new_project = ProjectModel(user_id=user_id, **project_data.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


def receive_projects(user_id: int, db: Session) -> List[ProjectOut]:
    return db.query(ProjectModel).filter(ProjectModel.user_id == user_id).all()


def receive_project_by_id(user_id: int, project_id: int, db: Session) -> ProjectOut | None:
    project = db.get(ProjectModel, project_id)
    if not project or project.user_id != user_id:
        return None

    return project


def change_project_info(user_id: int, new_project_info: ProjectEdit, db: Session) -> ProjectOut | None:
    project = db.query(ProjectModel).filter(ProjectModel.id == new_project_info.id).first()
    if not project or project.user_id != user_id:
        return None
    setattr(project, "neighbors_location", new_project_info.neighbors_location)
    setattr(project, "width_parcel", new_project_info.width_parcel)
    setattr(project, "length_parcel", new_project_info.length_parcel)

    db.commit()
    db.refresh(project)
    return project


def remove_project_by_id(user_id: int, project_id: int, db: Session) -> bool:
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project or project.user_id != user_id:
        return False

    db.delete(project)
    db.commit()
    return True
