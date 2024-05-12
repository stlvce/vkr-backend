from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config.repository_base import RepositoryBase
from app.config.models import NeighborModel

from .schemas import NeighborIn, LocationEnum


class NeighborRepository(RepositoryBase[NeighborModel, NeighborIn, NeighborIn]):
    def get_all_by_project_id(self, project_id: int, db: Session) -> list[NeighborModel]:
        query = select(self.model).where(
            self.model.project_id == project_id)
        res = db.execute(query)
        result = res.scalars().all()
        return result

    def create_multi(self, project_id: int, data_list: list[LocationEnum], db: Session):
        commit_list = []
        for item in data_list:
            commit_list.append(self.model(project_id=project_id, location=item))
        db.add_all(commit_list)
        db.commit()


neighbor_repository = NeighborRepository(NeighborModel)