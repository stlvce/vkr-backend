from app.database import Base
from typing import List
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped
from app.project.model import ProjectModel


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(32), unique=True, index=True)
    username = Column(String(32), unique=True)
    hashed_password = Column(String(64))
    # projects: Mapped[List[ProjectModel]] = relationship(back_populates="projects")
    projects = relationship("ProjectModel")
