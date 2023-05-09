from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from db_config.database import Base
from constants.loan_application_status_enum import LoanApplicationStatus

def generate_uuid():
    return str(uuid.uuid4())

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True,index = True, nullable=False, autoincrement=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=True)
    updated_at = Column(DateTime, onupdate=datetime.utcnow(), default=datetime.utcnow(), nullable=True)

class BusinessDetail(BaseModel):
    __tablename__ = "business_detail"

    business_uuid = Column(String(256), primary_key=True, index=True, nullable=False, default=generate_uuid)
    name = Column(String(256), unique=True, nullable=False)
    year_of_establishment = Column(Integer, nullable=False)

class LoanApplication(BaseModel):
    __tablename__ = "loan_application"
    
    application_uuid = Column(String(256), primary_key=True, nullable=False, default=generate_uuid)
    business_uuid = Column(String(256), nullable=False)
    accounting_provider_name = Column(String(256), nullable=True)
    loan_amount_requested = Column(Integer, nullable=True)
    application_status = Column(String(256), default=LoanApplicationStatus.NOT_SUBMITTED.value , nullable=False)
    accounting_balance_sheet_json = Column(JSON, nullable=True)
    pre_assessment_value = Column(JSON, nullable=True)
    amount_sanctioned = Column(Integer, nullable=True)
    decision_json = Column(JSON, nullable=True)


class AccountingProvider(BaseModel):
    __tablename__ = "accounting_provider"
    
    acconting_provider_name = Column(String(256), nullable=False)
    display = Column(String(256), default=False, nullable=False)


