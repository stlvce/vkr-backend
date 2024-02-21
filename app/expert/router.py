from fastapi import APIRouter, HTTPException, Depends
from .schemas import RuleCreate
from app.database import get_db, engine, Base
from .repository import add_new_rule

expert_router = APIRouter(prefix="/expert", tags=["Expert"])

Base.metadata.create_all(bind=engine)


@expert_router.post("/rule/add")
async def add_rule(rule: RuleCreate, db=Depends(get_db)):
    if len(rule.relation) != 2:
        raise HTTPException(status_code=400, detail="LENGTH_RELATION_LIST_NOT_EQUAL_2")
    new_rule = add_new_rule(rule, db)
    if not new_rule:
        raise HTTPException(status_code=400, detail="RULE_ALREADY_EXISTS")
    return new_rule
