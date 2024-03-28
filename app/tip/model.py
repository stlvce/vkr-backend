# from sqlalchemy import Integer, String, ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from app.config.database import Base
#
#
# class TipModel(Base):
#     __tablename__ = "tips"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"))
#     tip_text: Mapped[str] = mapped_column(String(100))
#
#     # TODO Mapped
#     project = relationship("ProjectModel", back_populates="tips")
#     # TODO many to many
#     buildings = relationship("BuildingModel", secondary="building_tip_table")
