from sqlalchemy.orm import Session

from model import db_model

def find_all_by_name(name: str, db: Session):
    return db.query(db_model.BusinessDetail).filter(db_model.BusinessDetail.name == name).all()

def find_by_business_uuid(business_uuid: str, db: Session):
    return db.query(db_model.BusinessDetail).filter(db_model.BusinessDetail.business_uuid == business_uuid).first()

def save(business_details : db_model.BusinessDetail, db: Session):
    db.add(business_details)
    db.commit()
    db.refresh(business_details)
    return business_details