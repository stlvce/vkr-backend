from sqlalchemy import exc
from sqlalchemy.orm import Session

from .model import RuleModel
from .schemas import RuleCreate


def receive_all_rules(db: Session):
    return db.query(RuleModel).all()


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


def delete_rule_by_id(rule_id: int, db: Session):
    db.query(RuleModel).filter(RuleModel.id == rule_id).delete()
    db.commit()
