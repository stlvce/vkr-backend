from sqlalchemy.orm import Session
from typing import Type

from app.config.models import TipModel

from .schemas import TipIn


def add_new_rule(tip_data: TipIn, db: Session):
    new_tip = TipModel(**tip_data.dict())
    db.add(new_tip)
    db.commit()
    db.refresh(new_tip)
    return new_tip


def receive_all_tips(project_id: int, db: Session) -> list[Type[TipModel]]:
    return db.query(TipModel).filter(TipModel.project_id == project_id).all()


def delete_rule_by_id(tip_id: int, db: Session):
    db.query(TipModel).filter(TipModel.id == tip_id).delete()
    db.commit()
