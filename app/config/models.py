from sqlalchemy import Integer, String, ForeignKey, SmallInteger, JSON, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
from datetime import datetime
from typing import List
from enum import Enum


class UserRole(Enum):
    user: str = "user"
    admin: str = "admin"


Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(32), unique=True)
    role: Mapped[UserRole] = mapped_column(String(32), default=UserRole.user, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(64))

    projects: Mapped[List["ProjectModel"]] = relationship("ProjectModel", back_populates="user",
                                                          cascade="all, delete-orphan")


class ProjectModel(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(80))
    description: Mapped[str] = mapped_column(String(200))
    width_parcel: Mapped[int] = mapped_column(SmallInteger)
    length_parcel: Mapped[int] = mapped_column(SmallInteger)
    neighbors_location: Mapped[List[str]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="projects")
    buildings: Mapped[List["BuildingModel"]] = relationship("BuildingModel", back_populates="project",
                                                            cascade="all, delete-orphan")
    tips: Mapped[List["TipModel"]] = relationship("TipModel", back_populates="project", cascade="all, delete-orphan")


class BuildingModel(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"))
    type: Mapped[str] = mapped_column(String(30), unique=True)
    title: Mapped[str] = mapped_column(String(40))
    start_x: Mapped[float] = mapped_column(Float)
    width_parcel: Mapped[int] = mapped_column(SmallInteger)
    length_parcel: Mapped[int] = mapped_column(SmallInteger)

    project: Mapped["ProjectModel"] = relationship("ProjectModel", back_populates="buildings")
    tips: Mapped[List["TipModel"]] = relationship("TipModel", secondary="building_tips")


class TipModel(Base):
    __tablename__ = "tips"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"))
    tip_text: Mapped[str] = mapped_column(String(100))

    project: Mapped["ProjectModel"] = relationship("ProjectModel", back_populates="tips")
    buildings = relationship("BuildingModel", secondary="building_tips")


class BuildingTips(Base):
    __tablename__ = "building_tips"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    building_id: Mapped[int] = mapped_column(Integer, ForeignKey("buildings.id"))
    tip_id: Mapped[int] = mapped_column(Integer, ForeignKey("tips.id"))


class RuleModel(Base):
    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    relation: Mapped[str] = mapped_column(String(50), unique=True)
    tip_text: Mapped[str] = mapped_column(String(100), unique=True)
    distance: Mapped[int] = mapped_column(SmallInteger)
