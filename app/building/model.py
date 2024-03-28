from sqlalchemy import Integer, String, SmallInteger, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geometry

from app.config.database import Base


# building_tip_table = Table(
#     "building_tip_table",
#     Base.metadata,
#     Column("building_id", ForeignKey("buildings.id"), primary_key=True),
#     Column("tip_id", ForeignKey("tips.id"), primary_key=True),
# )


class BuildingModel(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"))
    type: Mapped[str] = mapped_column(String(30), unique=True)
    title: Mapped[str] = mapped_column(String(40))
    start_point: Mapped[tuple[int, int]] = mapped_column(Geometry("Point"))
    width_parcel: Mapped[int] = mapped_column(SmallInteger)
    length_parcel: Mapped[int] = mapped_column(SmallInteger)

    # TODO Mapped
    project = relationship("ProjectModel", back_populates="buildings")
    # TODO many to many
    # tips = relationship("TipModel", secondary=building_tip_table, cascade="all, delete-orphan")
