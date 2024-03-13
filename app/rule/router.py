from fastapi import APIRouter, HTTPException, Depends
from app.database import get_db
from .schemas import RuleCreate
from .repository import add_new_rule

rule_router = APIRouter(prefix="/rule", tags=["Rules"])


@rule_router.post("/rule")
async def add_rule(rule: RuleCreate, db=Depends(get_db)):
    if len(rule.relation) != 2:
        raise HTTPException(status_code=400, detail="LENGTH_RELATION_LIST_NOT_EQUAL_2")
    new_rule = add_new_rule(rule, db)
    if not new_rule:
        raise HTTPException(status_code=400, detail="RULE_ALREADY_EXISTS")
    return new_rule
