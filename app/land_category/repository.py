from app.config.repository_base import RepositoryBase
from app.config.models import LandCategoryModel

from .schemas import LandCategoryIn, LandCategoryCreate


class LandCategoryRepository(RepositoryBase[LandCategoryModel, LandCategoryCreate, LandCategoryIn]):
    pass


land_category_repository = LandCategoryRepository(LandCategoryModel)
