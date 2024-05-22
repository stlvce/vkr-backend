from sqlalchemy.orm import Session
from typing import Type

from app.config.repository_base import RepositoryBase
from app.config.models import TipModel

from .schemas import TipIn, TipSaveIn

class TipRepository(RepositoryBase[TipModel, TipIn, TipIn]):
    def create_multi(self, tips_list: list[TipIn], db):
        commit_list = []
        for item in tips_list:
            commit_list.append(self.model(**item.dict()))
        db.add_all(commit_list)
        db.commit()

    def get_all(self, project_id: int, db: Session) -> list[Type[TipModel]]:
        return db.query(self.model).where(self.model.project_id == project_id).all()

    def delete_multi(self, tips_list: list[TipModel], db: Session):
        for tip in tips_list:
            db.delete(tip)
        db.commit()

tip_repository = TipRepository(TipModel)
