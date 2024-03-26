from fastapi import APIRouter, HTTPException, Depends

from app.config.database import get_db

from .schemas import RuleCreate
from .repository import add_new_rule, receive_all_rules, delete_rule_by_id

rule_router = APIRouter(prefix="/api/rule", tags=["Rules"])


@rule_router.get("/all")
async def get_rules(db=Depends(get_db)):
    return receive_all_rules(db)


@rule_router.post("")
async def create_rule(rule: RuleCreate, db=Depends(get_db)):
    if len(rule.relation) != 2:
        raise HTTPException(status_code=400, detail="LENGTH_RELATION_LIST_NOT_EQUAL_2")
    new_rule = add_new_rule(rule, db)
    if not new_rule:
        raise HTTPException(status_code=400, detail="RULE_ALREADY_EXISTS")
    return new_rule


@rule_router.put("/{rule_id}")
async def edit_rule(rule_id: int, db=Depends(get_db)):
    return "edit rule"


@rule_router.delete("/{rule_id}")
async def delete_rule(rule_id: int, db=Depends(get_db)):
    delete_rule_by_id(rule_id, db)
    return "OK"
