from app.config.repository_base import RepositoryBase
from app.config.models import DocumentModel

from .schemas import DocumentIn, DocumentEdit


class DocumentRepository(RepositoryBase[DocumentModel, DocumentIn, DocumentEdit]):
    pass


document_repository = DocumentRepository(DocumentModel)
