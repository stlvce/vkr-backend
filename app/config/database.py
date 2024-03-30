from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import db_settings

engine = create_engine(
    db_settings.db_url
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
