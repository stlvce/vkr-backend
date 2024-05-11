from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.config.repository_base import RepositoryBase
from app.config.models import DocumentModel, DocumentNorms, TypePermissionDocuments


from .schemas import DocumentIn, DocumentEdit, DocTypePermissionPin, DocNormPin


class DocumentRepository(RepositoryBase[DocumentModel, DocumentIn, DocumentEdit]):
    def get_type_permissions_norms(self, document_id: int, db: Session):
        query = select(self.model).filter(
            self.model.id == document_id).options(
            selectinload(self.model.type_permissions)).options(selectinload(self.model.norms))
        res = db.execute(query)
        result = res.unique().scalars().first()
        return result

    def type_permission_pin(self, pin_data: DocTypePermissionPin, db: Session):
        db_doc_type_permission = TypePermissionDocuments(**pin_data.dict())
        db.add(db_doc_type_permission)
        db.commit()

    def type_permission_pin_delete(self, pin_data: DocTypePermissionPin, db: Session) -> TypePermissionDocuments | None:
        q = select(TypePermissionDocuments).where(TypePermissionDocuments.type_permission_id == pin_data.type_permission_id,
                                              TypePermissionDocuments.document_id == pin_data.document_id)
        result = db.execute(q)
        obj = result.scalar()

        if not obj:
            return None

        db.delete(obj)
        db.commit()

        return obj

    def norm_pin(self, pin_data: DocNormPin, db: Session):
        db_documents_norms = DocumentNorms(**pin_data.dict())
        db.add(db_documents_norms)
        db.commit()

    def norm_pin_delete(self, pin_data: DocNormPin, db: Session):
        q = select(DocumentNorms).where(DocumentNorms.document_id == pin_data.document_id,
                                              DocumentNorms.norm_id == pin_data.norm_id)
        result = db.execute(q)
        obj = result.scalar()

        if not obj:
            return None

        db.delete(obj)
        db.commit()

        return obj

document_repository = DocumentRepository(DocumentModel)
