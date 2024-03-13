from sqlalchemy import exc
from sqlalchemy.orm import Session
from .model import UserModel
from .schemas import UserCreate
from app.auth.service import get_password_hash


def add_new_user(new_user: UserCreate, db: Session):
    try:
        hashed_password = get_password_hash(new_user.password)
        db_user = UserModel(email=new_user.email, username=new_user.username, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except exc.IntegrityError:
        return None


def get_user_by_username(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()
