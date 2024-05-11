from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.config.models import NormModel, DocumentNorms, TypePermissionNorms
from app.config.repository_base import RepositoryBase, CreateSchemaType

from .schemas import NormIn, NormOut, NormUpdate, NormWithTypePermissions, NormWithTypeDocuments, NormTypePermissionPin


class NormRepository(RepositoryBase[NormModel, NormIn, NormUpdate]):
    def create(self, obj_in: CreateSchemaType, db: Session):
        relation = "-".join(obj_in.relation)
        db_norm = NormModel(relation=relation, description=obj_in.description, distance=obj_in.distance, type=obj_in.type, priority=obj_in.priority)
        db.add(db_norm)
        db.commit()
        db.refresh(db_norm)

        db_types_norms = TypePermissionNorms(type_permission_id=obj_in.type_permission_id, norm_id=db_norm.id)
        db_documents_norms = DocumentNorms(document_id=obj_in.document_id, norm_id=db_norm.id)
        db.add_all([db_types_norms, db_documents_norms])
        db.commit()

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

    def type_permission_pin(self, pin_data: list[NormTypePermissionPin], db: Session):
        commit_list = []
        for item in pin_data:
            commit_list.append(TypePermissionNorms(**item.dict()))
        db.add_all(commit_list)
        db.commit()

    def type_permission_pin_delete(self, pin_id: int, db: Session) -> NormTypePermissionPin | None:
        obj = db.get(TypePermissionNorms, pin_id)

        if not obj:
            return None

        db.delete(obj)
        db.commit()

        return obj


norm_repository = NormRepository(NormModel)
