from sqlalchemy import exc
from sqlalchemy.orm import Session
from .model import UserModel
from .schemas import UserCreate


def add_new_user(new_user: UserCreate, db: Session):
    try:
        db_user = UserModel(email=new_user.email, username=new_user.username, password=new_user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except exc.IntegrityError:
        return None
