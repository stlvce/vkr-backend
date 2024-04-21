from sqlalchemy import exc
from sqlalchemy.orm import Session

from app.config.models import NormModel

from .schemas import NormCreate, NormOut


def add_new_norm(new_norm: NormCreate, db: Session):
    try:
        relation = "-".join(new_norm.relation)
        db_norm = NormModel(relation=relation, description=new_norm.description, distance=new_norm.distance)
        db.add(db_norm)
        db.commit()
        db.refresh(db_norm)
        return db_norm
    except exc.IntegrityError:
        return None


def receive_all_norms(db: Session):
    return db.query(NormModel).all()


def receive_norm_by_id(norm_id: int, db: Session) -> NormOut:
    norm = db.get(NormModel, norm_id)
    return norm


def receive_norm_by_relation(relation: str, db: Session) -> NormOut:
    norm = db.query(NormModel).filter(NormModel.relation == relation).first()
    return norm


def change_norm_info(new_norm_info: NormOut, db: Session):
    norm = db.query(NormModel).filter(NormModel.id == new_norm_info.id).first()
    if not norm:
        return None
    delattr(new_norm_info, "id")
    setattr(norm, "relation", "-".join(new_norm_info.relation))
    setattr(norm, "distance", new_norm_info.distance)
    setattr(norm, "description", new_norm_info.description)
    db.commit()
    db.refresh(norm)
    return norm


def delete_norm_by_id(norm_id: int, db: Session):
    db.query(NormModel).filter(NormModel.id == norm_id).delete()
    db.commit()
