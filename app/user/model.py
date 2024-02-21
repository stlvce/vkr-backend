from app.database import Base
from sqlalchemy import Column, Integer, String


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(32), unique=True, index=True)
    username = Column(String(32), unique=True)
    password = Column(String(32))
