from sqlalchemy import Integer, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.config.database import Base


class RuleModel(Base):
    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    relation: Mapped[str] = mapped_column(String(50), unique=True)
    tip_text: Mapped[str] = mapped_column(String(100), unique=True)
    distance: Mapped[int] = mapped_column(SmallInteger)
