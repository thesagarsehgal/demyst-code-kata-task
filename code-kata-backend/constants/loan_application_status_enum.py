
from enum import Enum


class LoanApplicationStatus(Enum):
    NOT_SUBMITTED = "not_submitted"
    BALANCE_SHEET_FETCHED = "balance_sheet_fetched"
    SUBMITTED = "submitted"
    LOAN_DECISION_COMPLETE = "loan_decision_complete" 
    
 