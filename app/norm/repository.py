from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.config.models import NormModel
from app.config.repository_base import RepositoryBase, CreateSchemaType

from .schemas import NormIn, NormOut, NormUpdate, NormWithTypePermissions, NormWithTypeDocuments


class NormRepository(RepositoryBase[NormModel, NormIn, NormUpdate]):
    def create(self, obj_in: CreateSchemaType, db: Session):
        relation = "-".join(obj_in.relation)
        db_norm = NormModel(relation=relation, description=obj_in.description, distance=obj_in.distance)
        db.add(db_norm)
        db.commit()
        db.refresh(db_norm)
        return db_norm

    def get_by_relation(self, relation: str, db: Session) -> NormOut | None:
        norm = db.query(NormModel).filter(NormModel.relation == relation).first()

        if not norm:
            return None

        return norm

    def get_type_permissions(self, norm_id: int, db: Session) -> NormWithTypePermissions:
        query = select(NormModel).filter(
            NormModel.id == norm_id).options(
            selectinload(NormModel.type_permissions))
        res = db.execute(query)
        result = res.unique().scalars().first()
        return result

    def get_documents(self, norm_id: int, db: Session) -> NormWithTypeDocuments:
        query = select(NormModel).filter(
            NormModel.id == norm_id).options(
            selectinload(NormModel.documents))
        res = db.execute(query)
        result = res.unique().scalars().first()
        return result


norm_repository = NormRepository(NormModel)
