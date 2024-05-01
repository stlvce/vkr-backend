from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.config.models import TypePermissionModel, LandCategoryModel, DocumentModel
from app.config.repository_base import RepositoryBase

from .schemas import (TypePermissionIn, TypePermissionCreate, TypePermissionOutWithCategoryOut, TypePermissionWithNorms,
                      TypePermissionWithDocuments, TypePermissionDocumentsNormsOut)


class TypePermissionRepository(RepositoryBase[TypePermissionModel, TypePermissionCreate, TypePermissionIn]):
    def get_all_with_categories(self, db: Session) -> list[TypePermissionOutWithCategoryOut]:
        q = db.query(LandCategoryModel, self.model).join(self.model,
                                                         self.model.land_category_id == LandCategoryModel.id,
                                                         isouter=True)
        result = q.all()
        res = []
        for item, item2 in result:
            res.append({"id": item2.id, "land_category_id": item2.land_category_id, "title": item2.title,
                        "image_url": item2.image_url,
                        "category_title": item.category_title, })

        return res

    def get_all_by_land_category_id(self, land_category_id: int, db: Session) -> list[TypePermissionModel]:
        return db.query(self.model).filter(self.model.land_category_id == land_category_id).all()

    def get_norms(self, type_permission_id: int, db: Session) -> TypePermissionWithNorms | None:
        query = select(self.model).filter(
            self.model.id == type_permission_id).options(
            selectinload(self.model.norms))
        res = db.execute(query)
        result = res.unique().scalars().first()
        return result

    def get_documents(self, type_permission_id: int, db: Session) -> TypePermissionWithDocuments | None:
        query = select(self.model).filter(
            self.model.id == type_permission_id).options(
            selectinload(self.model.documents))
        res = db.execute(query)
        result = res.unique().scalars().first()
        return result

    def get_documents_norms(self, type_permission_id: int, db: Session) -> TypePermissionDocumentsNormsOut | None:
        query = select(self.model).filter(
            self.model.id == type_permission_id).options(
            selectinload(self.model.documents).subqueryload(DocumentModel.norms))
        res = db.execute(query)
        result = res.unique().scalars().first()
        return result


type_permission_repository = TypePermissionRepository(TypePermissionModel)
