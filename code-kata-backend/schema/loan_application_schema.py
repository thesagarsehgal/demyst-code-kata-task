from typing import Optional
from pydantic import BaseModel, Field
from constants.accounting_provider_enum import AccountingProviderEnum

from constants.loan_application_status_enum import LoanApplicationStatus

# request schema
class CreateLoanApplicationRequestSchema(BaseModel):
    business_uuid: str

class UpdateLoanApplicationRequestSchema(BaseModel):
    application_uuid: str
    accounting_provider_name: Optional[AccountingProviderEnum]
    loan_amount: Optional[int] 
    # business_name: Optional[str]
    # year_of_establishment: Optional[int] 
    
class SubmitLoanApplicationRequestSchema(BaseModel):
    application_uuid: str

    
# response schema
class CreateLoanApplicationResponseSchema(BaseModel):
    business_uuid: str
    application_uuid: str 

class UpdateLoanApplicationResponseSchema(BaseModel):
    application_uuid: Optional[str]
    business_uuid: Optional[str]
    loan_amount: Optional[int] 
    application_status: Optional[LoanApplicationStatus] 
    accounting_provider_name: Optional[AccountingProviderEnum]
    # business_name: Optional[str]
    # year_of_establishment: Optional[int] 

class SubmitLoanApplicationResponseSchema(BaseModel):
    application_uuid: str
    business_uuid: str
    loan_amount: int
    application_status: LoanApplicationStatus
    accounting_provider_name: AccountingProviderEnum
    pre_assessment_value: int
    decision: dict
    loan_amount_sanctioned: int 