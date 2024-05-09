from fastapi.encoders import jsonable_encoder
from typing import Generic, TypeVar, Type
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .models import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class RepositoryBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, obj_in: CreateSchemaType, db: Session):
        try:
            db_obj = self.model(**obj_in.dict())
            db.add(db_obj)
            db.commit()
            return True
        except Exception as e:
            # TODO сделать нормальную обработку
            return None

    def get(self, obj_id: int, db: Session) -> ModelType | None:
        model_obj = db.get(self.model, obj_id)
        if not model_obj:
            return None

        return model_obj

    def get_all(self, db: Session, offset: int = 0,
                limit: int = 100) -> list[ModelType]:
        return db.query(self.model).all()

    def update(self, obj_id: int, obj_in: UpdateSchemaType, db: Session) -> ModelType | None:
        db_obj = self.get(obj_id, db)

        if not db_obj:
            return None

        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict()

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.commit()
        return db_obj

    def delete(self, obj_id: int, db: Session) -> ModelType | None:
        # try:

        obj = db.get(self.model, obj_id)

        if not obj:
            return None

        db.delete(obj)
        db.commit()

        return obj
