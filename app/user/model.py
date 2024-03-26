from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.config.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(32), unique=True, index=True)
    username = Column(String(32), unique=True)
    hashed_password = Column(String(64))
    projects = relationship("ProjectModel")
