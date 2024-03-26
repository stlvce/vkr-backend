from sqlalchemy import Column, Integer, JSON, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base


class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    neighbors_location = Column(JSON)
    width_parcel = Column(SmallInteger)
    length_parcel = Column(SmallInteger)

    user = relationship("UserModel", back_populates="projects")
