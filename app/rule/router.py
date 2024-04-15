from fastapi import APIRouter, HTTPException, Depends

from app.config.database import get_db

from .schemas import RuleCreate, RuleOut
from .repository import add_new_rule, receive_all_rules, delete_rule_by_id, change_rule_info, receive_rule_by_id

rule_router = APIRouter()


@rule_router.get("/all")
async def get_rules(db=Depends(get_db)):
    return receive_all_rules(db)


@rule_router.get("/{rule_id}")
async def get_rule_by_id(rule_id: int, db=Depends(get_db)):
    return receive_rule_by_id(rule_id, db)


@rule_router.post("")
async def create_rule(rule: RuleCreate, db=Depends(get_db)):
    if len(rule.relation) != 2:
        raise HTTPException(status_code=400, detail="LENGTH_RELATION_LIST_NOT_EQUAL_2")
    new_rule = add_new_rule(rule, db)
    if not new_rule:
        raise HTTPException(status_code=400, detail="RULE_ALREADY_EXISTS")
    return new_rule


@rule_router.put("")
async def edit_rule(new_project_info: RuleOut, db=Depends(get_db)):
    rule = change_rule_info(new_project_info, db)
    if not rule:
        raise HTTPException(status_code=400)

    return rule


@rule_router.delete("/{rule_id}")
async def delete_rule(rule_id: int, db=Depends(get_db)):
    delete_rule_by_id(rule_id, db)
    return "OK"
