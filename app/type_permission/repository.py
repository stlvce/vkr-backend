from sqlalchemy.orm import Session

from app.config.models import TypePermissionModel, LandCategoryModel
from app.config.repository_base import RepositoryBase

from .schemas import TypePermissionIn, TypePermissionOutWithCategoryOut


class TypePermissionRepository(RepositoryBase[TypePermissionModel, TypePermissionIn, TypePermissionIn]):
    def get_all_with_categories(self, db: Session) -> list[TypePermissionOutWithCategoryOut]:
        q = db.query(LandCategoryModel, self.model).join(self.model,
                                                         self.model.land_category_id == LandCategoryModel.id,
                                                         isouter=True)
        result = q.all()
        res = []
        for item, item2 in result:
            res.append({"id": item2.id, "land_category_id": item2.land_category_id, "title": item2.title,
                        "category_title": item.category_title, })

        return res

    def get_all_by_land_category_id(self, land_category_id: int, db: Session) -> list[TypePermissionModel]:
        return db.query(self.model).filter(self.model.land_category_id == land_category_id).all()


type_permission_repository = TypePermissionRepository(TypePermissionModel)
