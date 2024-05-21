from sqlalchemy import exc
from sqlalchemy.orm import Session

from app.config.repository_base import RepositoryBase
from app.config.models import UserModel
from app.auth.service import get_password_hash

from .schemas import UserIn, UserOut, UserCreate, UserUpdate


class UserRepository(RepositoryBase[UserModel, UserCreate, UserUpdate]):
    def get_by_username(self, username: str, db: Session) -> UserOut | None:
        return db.query(self.model).where(self.model.username == username).first()

user_repository = UserRepository(UserModel)
