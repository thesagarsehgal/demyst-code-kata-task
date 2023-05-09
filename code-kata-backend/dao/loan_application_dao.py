from sqlalchemy.orm import Session

from model import db_model


def find_by_application_uuid(loan_application_uuid: str, db: Session):
    return db.query(db_model.LoanApplication).filter(db_model.LoanApplication.application_uuid == loan_application_uuid).first()

def save(business_details : db_model.LoanApplication, db: Session):
    db.add(business_details)
    db.commit()
    db.refresh(business_details)
    return business_details