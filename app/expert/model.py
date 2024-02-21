from app.database import Base
from sqlalchemy import Column, Integer, String, SmallInteger, VARCHAR


class RuleModel(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True)
    relation = Column(VARCHAR(50), unique=True)
    tip_text = Column(VARCHAR(100), unique=True)
    distance = Column(SmallInteger)
