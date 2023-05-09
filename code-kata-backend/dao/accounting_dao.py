from sqlalchemy.orm import Session

from model import db_model

def find_all_where_display_true(db: Session):
    return db.query(db_model.AccountingProvider).filter(db_model.AccountingProvider.display == True).all()

def save(accounting_provider : db_model.AccountingProvider, db: Session):
    db.add(accounting_provider)
    db.commit()
    db.refresh(accounting_provider)
    return accounting_provider