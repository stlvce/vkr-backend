from sqlalchemy import Column, Integer, SmallInteger, VARCHAR

from app.config.database import Base


class RuleModel(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True)
    relation = Column(VARCHAR(50), unique=True)
    tip_text = Column(VARCHAR(100), unique=True)
    distance = Column(SmallInteger)
