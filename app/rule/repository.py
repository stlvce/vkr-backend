from sqlalchemy import exc
from sqlalchemy.orm import Session

from app.config.models import RuleModel

from .schemas import RuleCreate, RuleOut


def add_new_rule(new_rule: RuleCreate, db: Session):
    try:
        relation = "-".join(new_rule.relation)
        db_rule = RuleModel(relation=relation, tip_text=new_rule.tip_text, distance=new_rule.distance)
        db.add(db_rule)
        db.commit()
        db.refresh(db_rule)
        return db_rule
    except exc.IntegrityError:
        return None


def receive_all_rules(db: Session):
    return db.query(RuleModel).all()


def receive_rule_by_id(rule_id: int, db: Session) -> RuleOut:
    rule = db.get(RuleModel, rule_id)
    return rule


def receive_rule_by_relation(relation: str, db: Session) -> RuleOut:
    rule = db.query(RuleModel).filter(RuleModel.relation == relation).first()
    return rule


def change_rule_info(new_rule_info: RuleOut, db: Session):
    rule = db.query(RuleModel).filter(RuleModel.id == new_rule_info.id).first()
    if not rule:
        return None
    delattr(new_rule_info, "id")
    setattr(rule, "relation", "-".join(new_rule_info.relation))
    setattr(rule, "distance", new_rule_info.distance)
    setattr(rule, "tip_text", new_rule_info.tip_text)
    db.commit()
    db.refresh(rule)
    return rule


def delete_rule_by_id(rule_id: int, db: Session):
    db.query(RuleModel).filter(RuleModel.id == rule_id).delete()
    db.commit()
