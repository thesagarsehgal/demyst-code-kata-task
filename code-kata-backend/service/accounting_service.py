
from fastapi import HTTPException, status
from constants.loan_application_status_enum import LoanApplicationStatus
from dao import accounting_dao, loan_application_dao
from model import db_model
from schema import accounting_schema
from sqlalchemy.orm import Session

from service.accounting_provider.accounting_provider_factory import AccountingProviderFactory


def get_all_providers(db: Session):
    all_accounting_providers = accounting_dao.find_all_where_display_true(db)
    return accounting_schema.AllAccountingProviderResponseSchema(
        all_providers= [ accounting_schema.AccountingProvider(
                accounting_provider_name=provider.acconting_provider_name
            ) for provider in all_accounting_providers ]
    )

def register_providers(name: str, db: Session):
    accounting_provider = accounting_dao.save(db_model.AccountingProvider(acconting_provider_name=name.upper(), display=True), db)
    all_accounting_providers = accounting_dao.find_all_where_display_true(db)
    return accounting_schema.AllAccountingProviderResponseSchema(
        all_providers= [ accounting_schema.AccountingProvider(
                accounting_provider_name=provider.acconting_provider_name
            ) for provider in all_accounting_providers ]
    )

def get_balance_sheet(get_balance_sheet_request_schema : accounting_schema.GetBalanceSheetRequestSchema , db: Session):
    # verify if application exists
    application_in_db = loan_application_dao.find_by_application_uuid(get_balance_sheet_request_schema.application_uuid, db)
    if(application_in_db == None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND ,
            detail="Application with this uuid not found"
        )
    if(application_in_db.accounting_provider_name == None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND ,
            detail="Accounting Provider not found for the application"
        )
    if(application_in_db.business_uuid == None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND ,
            detail="Business UUID not found for the application"
        )
    
    balance_sheet_extracted = True
    balance_sheet = []
    try:
        accounting_provider = AccountingProviderFactory().get(application_in_db.accounting_provider_name)
        balance_sheet = accounting_provider.extract_accounting_balance_sheet()
        application_in_db.accounting_balance_sheet_json = balance_sheet
        application_in_db.application_status = LoanApplicationStatus.BALANCE_SHEET_FETCHED.value
        loan_application_dao.save(application_in_db, db)
    except Exception as e:
        balance_sheet_extracted = False
        
    
    return accounting_schema.GetBalanceSheetResponseSchema(
        application_uuid = get_balance_sheet_request_schema.application_uuid,
        balance_sheet_extracted = balance_sheet_extracted,
        balance_sheet_data = [accounting_schema.BalanceSheetMonthlyData(
            year = month_data["year"], 
            month = month_data["month"], 
            assetsValue= month_data["assetsValue"], 
            profitOrLoss = month_data["profitOrLoss"]
        ) for month_data in balance_sheet] 
    )
    
    
    
    
    
    