from sqlalchemy import Integer, JSON, SmallInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from app.config.database import Base


class ProjectModel(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    neighbors_location: Mapped[List[str]] = mapped_column(JSON)
    width_parcel: Mapped[int] = mapped_column(SmallInteger)
    length_parcel: Mapped[int] = mapped_column(SmallInteger)

    # TODO Mapped
    user = relationship("UserModel", back_populates="projects")
    buildings = relationship("BuildingModel", back_populates="project", cascade="all, delete-orphan")
    tips = relationship("TipModel", back_populates="project", cascade="all, delete-orphan")
