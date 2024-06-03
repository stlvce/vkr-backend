from sqlalchemy.orm import Session
from typing import Type

from app.config.repository_base import RepositoryBase
from app.config.models import TipModel, BuildingTips

from .schemas import TipIn, TipSaveIn

class TipRepository(RepositoryBase[TipModel, TipIn, TipIn]):
    def create_multi(self, project_id: int, tips_list: list[TipSaveIn], db: Session):
        for item in tips_list:
            new_tip_dict = item.dict()
            new_tip_dict["project_id"] = project_id
            buildings_id_list = new_tip_dict.pop("buildings")
            new_tip = self.model(**new_tip_dict)
            db.add(new_tip)
            db.flush()
            db.add_all([BuildingTips(tip_id=new_tip.id, building_id=el) for el in buildings_id_list])
        db.commit()
        

    def get_all(self, project_id: int, db: Session) -> list[Type[TipModel]]:
        return db.query(self.model).where(self.model.project_id == project_id).all()

    def delete_multi(self, tips_list: list[TipModel], db: Session):
        for tip in tips_list:
            db.delete(tip)
        db.commit()

tip_repository = TipRepository(TipModel)
