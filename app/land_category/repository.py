from app.config.repository_base import RepositoryBase
from app.config.models import LandCategoryModel

from .schemas import LandCategoryIn


class LandCategoryRepository(RepositoryBase[LandCategoryModel, LandCategoryIn, LandCategoryIn]):
    pass


land_category_repository = LandCategoryRepository(LandCategoryModel)
