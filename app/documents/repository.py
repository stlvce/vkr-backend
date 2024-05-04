from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload, joinedload

from app.config.repository_base import RepositoryBase
from app.config.models import DocumentModel

from .schemas import DocumentIn, DocumentEdit


class DocumentRepository(RepositoryBase[DocumentModel, DocumentIn, DocumentEdit]):
    def get_type_permissions_norms(self, document_id: int, db: Session):
        query = select(self.model).filter(
            self.model.id == document_id).options(
            selectinload(self.model.type_permissions)).options(selectinload(self.model.norms))
        res = db.execute(query)
        result = res.unique().scalars().first()
        return result


document_repository = DocumentRepository(DocumentModel)
