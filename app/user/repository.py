from sqlalchemy import exc
from sqlalchemy.orm import Session

from app.config.repository_base import RepositoryBase
from app.config.models import UserModel
from app.auth.service import get_password_hash

from .schemas import UserIn, UserOut, UserCreate, UserUpdate


class UserRepository(RepositoryBase[UserModel, UserCreate, UserUpdate]):
    def get_by_username(self, username: str, db: Session) -> UserOut | None:
        return db.query(self.model).where(self.model.username == username).first()
    
    def update_user_password(self, user_id: int, new_password: str, db: Session) -> UserOut | None:
        db_obj = self.get(user_id, db)

        if not db_obj:
            return None

        setattr(db_obj, "hashed_password", new_password)

        db.commit()
        return db_obj

user_repository = UserRepository(UserModel)
