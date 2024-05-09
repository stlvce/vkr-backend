from app.config.repository_base import RepositoryBase
from app.config.models import MaterialModel

from .schemas import MaterialIn


class MaterialRepository(RepositoryBase[MaterialModel, MaterialIn, MaterialIn]):
    pass


material_repository = MaterialRepository(MaterialModel)