from sqlalchemy.orm import Session
from .model import User
from .schemas import UserCreate


def add_new_user(db: Session, new_user: UserCreate):
    db_user = User(email=new_user.email, username=new_user.username, password=new_user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
