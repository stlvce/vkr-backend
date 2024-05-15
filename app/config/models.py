from sqlalchemy import Integer, String, ForeignKey, SmallInteger, JSON, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from typing import List
from enum import Enum


class UserRole(Enum):
    user: str = "user"
    admin: str = "admin"

    def __str__(self):
        return self.value

    def __repr__(self):
        return repr(self.value)


Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    email: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(32), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(64))
    role: Mapped[UserRole] = mapped_column(String(32), default=UserRole.user, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    projects: Mapped[List["ProjectModel"]] = relationship("ProjectModel", back_populates="user",
                                                          cascade="all, delete-orphan")


class ProjectModel(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    title: Mapped[str] = mapped_column(String(80))
    description: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    changed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="projects")
    land: Mapped["LandModel"] = relationship("LandModel", back_populates="project", cascade="all, delete-orphan")
    buildings: Mapped[List["BuildingModel"]] = relationship("BuildingModel", back_populates="project",
                                                            cascade="all, delete-orphan")
    tips: Mapped[List["TipModel"]] = relationship("TipModel", back_populates="project", cascade="all, delete-orphan")
    neighbours: Mapped[List["NeighborModel"]] = relationship("NeighborModel", back_populates="project",
                                                             cascade="all, delete-orphan")


class LandModel(Base):
    __tablename__ = "lands"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"))
    land_category_id: Mapped[int] = mapped_column(Integer, ForeignKey("land_categories.id"))
    type_permission_id: Mapped[int] = mapped_column(Integer, ForeignKey("type_permissions.id"))

    width_parcel: Mapped[int] = mapped_column(SmallInteger)
    length_parcel: Mapped[int] = mapped_column(SmallInteger)
    red_borders: Mapped[List[str]] = mapped_column(JSON)

    project: Mapped["ProjectModel"] = relationship("ProjectModel", back_populates="land")
    land_category: Mapped["LandCategoryModel"] = relationship("LandCategoryModel", back_populates="lands")
    type_permission: Mapped["TypePermissionModel"] = relationship("TypePermissionModel", back_populates="lands")


class NeighborModel(Base):
    __tablename__ = "neighbours"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"))

    location: Mapped[str] = mapped_column(String(20))

    project: Mapped["ProjectModel"] = relationship("ProjectModel", back_populates="neighbours")
    buildings: Mapped[List["BuildingModel"]] = relationship("BuildingModel", back_populates="neighbor",
                                                            cascade="all, delete-orphan")


class BuildingModel(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"))
    material_id: Mapped[int] = mapped_column(Integer, ForeignKey("materials.id"))
    neighbor_id: Mapped[int] = mapped_column(Integer, ForeignKey("neighbours.id"), nullable=True, default=None)

    type: Mapped[str] = mapped_column(String(30))
    title: Mapped[str] = mapped_column(String(40))
    start_x: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    start_y: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    width: Mapped[int] = mapped_column(SmallInteger)
    length: Mapped[int] = mapped_column(SmallInteger)
    height: Mapped[int] = mapped_column(SmallInteger)

    project: Mapped["ProjectModel"] = relationship("ProjectModel", back_populates="buildings")
    material: Mapped["MaterialModel"] = relationship("MaterialModel", back_populates="buildings")
    tips: Mapped[List["TipModel"]] = relationship("TipModel", secondary="building_tips", back_populates="buildings")
    neighbor: Mapped["NeighborModel"] = relationship("NeighborModel", back_populates="buildings")


class TipModel(Base):
    __tablename__ = "tips"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"))
    norm_id: Mapped[int] = mapped_column(Integer, ForeignKey("norms.id"))

    description: Mapped[str] = mapped_column(String(200))
    priority: Mapped[int] = mapped_column(String(10))
    current_distance: Mapped[int] = mapped_column(SmallInteger)
    type: Mapped[str] = mapped_column(String(30))

    project: Mapped["ProjectModel"] = relationship("ProjectModel", back_populates="tips")
    buildings = relationship("BuildingModel", secondary="building_tips", back_populates="tips")
    norm: Mapped["NormModel"] = relationship("NormModel", back_populates="tips")


class BuildingTips(Base):
    __tablename__ = "building_tips"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    building_id: Mapped[int] = mapped_column(Integer, ForeignKey("buildings.id"))
    tip_id: Mapped[int] = mapped_column(Integer, ForeignKey("tips.id"))


class LandCategoryModel(Base):
    __tablename__ = "land_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    category_title: Mapped[str] = mapped_column(String(40), unique=True)
    image_url: Mapped[str] = mapped_column(String(150))

    type_permissions: Mapped[List["TypePermissionModel"]] = relationship("TypePermissionModel",
                                                                         back_populates="land_category",
                                                                         cascade="all, delete-orphan")
    lands: Mapped[List["LandModel"]] = relationship("LandModel", back_populates="land_category")


class TypePermissionModel(Base):
    __tablename__ = "type_permissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    land_category_id: Mapped[int] = mapped_column(Integer, ForeignKey("land_categories.id"))

    title: Mapped[str] = mapped_column(String(40))
    code: Mapped[str] = mapped_column(String(10))
    image_url: Mapped[str] = mapped_column(String(150))

    land_category: Mapped["LandCategoryModel"] = relationship("LandCategoryModel", back_populates="type_permissions")
    lands: Mapped[List["LandModel"]] = relationship("LandModel", back_populates="type_permission")
    init_buildings: Mapped[List["InitBuildingModel"]] = relationship("InitBuildingModel",
                                                                     back_populates="type_permission",
                                                                     cascade="all, delete-orphan")
    norms: Mapped[List["NormModel"]] = relationship(secondary="type_permission_norms",
                                                    back_populates="type_permissions")
    documents: Mapped[List["DocumentModel"]] = relationship(secondary="type_permission_documents",
                                                            back_populates="type_permissions")


class InitBuildingModel(Base):
    __tablename__ = "init_buildings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type_permission_id: Mapped[int] = mapped_column(Integer, ForeignKey("type_permissions.id"))

    type: Mapped[str] = mapped_column(String(30), unique=True)
    title: Mapped[str] = mapped_column(String(40))
    min_length: Mapped[int] = mapped_column(SmallInteger)
    max_length: Mapped[int] = mapped_column(SmallInteger)
    min_width: Mapped[int] = mapped_column(SmallInteger)
    max_width: Mapped[int] = mapped_column(SmallInteger)

    type_permission: Mapped["TypePermissionModel"] = relationship("TypePermissionModel",
                                                                  back_populates="init_buildings")


class NormModel(Base):
    __tablename__ = "norms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    relation: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(200), unique=True)
    distance: Mapped[int] = mapped_column(SmallInteger)
    priority: Mapped[int] = mapped_column(String(10))
    type: Mapped[str] = mapped_column(String(30))

    tips: Mapped[List["TipModel"]] = relationship("TipModel", back_populates="norm", cascade="all, delete-orphan")
    type_permissions: Mapped[List["TypePermissionModel"]] = relationship(secondary="type_permission_norms",
                                                                         back_populates="norms")
    documents: Mapped[List["DocumentModel"]] = relationship(secondary="document_norms", back_populates="norms")


class TypePermissionNorms(Base):
    __tablename__ = "type_permission_norms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type_permission_id: Mapped[int] = mapped_column(Integer, ForeignKey("type_permissions.id"))
    norm_id: Mapped[int] = mapped_column(Integer, ForeignKey("norms.id"))


class DocumentModel(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str] = mapped_column(String(90), unique=True)
    file_type: Mapped[str] = mapped_column(String(30))
    link: Mapped[str] = mapped_column(String(150), unique=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    type_permissions: Mapped[List["TypePermissionModel"]] = relationship("TypePermissionModel",
                                                                         secondary="type_permission_documents",
                                                                         back_populates="documents")
    norms: Mapped[List["NormModel"]] = relationship("NormModel", secondary="document_norms", back_populates="documents")


class DocumentNorms(Base):
    __tablename__ = "document_norms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    document_id: Mapped[int] = mapped_column(Integer, ForeignKey("documents.id"))
    norm_id: Mapped[int] = mapped_column(Integer, ForeignKey("norms.id"))


class TypePermissionDocuments(Base):
    __tablename__ = "type_permission_documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type_permission_id: Mapped[int] = mapped_column(Integer, ForeignKey("type_permissions.id"))
    document_id: Mapped[int] = mapped_column(Integer, ForeignKey("documents.id"))


class MaterialModel(Base):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    material_title: Mapped[str] = mapped_column(String(90), unique=True)
    additional_distance: Mapped[int] = mapped_column(SmallInteger)

    buildings: Mapped[List["BuildingModel"]] = relationship("BuildingModel", back_populates="material")