from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from constants.loan_application_status_enum import LoanApplicationStatus
from constants.request_enum import RequestType
from schema import loan_application_schema
from dao import loan_application_dao, business_dao
from model import db_model
from utils import loan_application_utils
from utils.common_utils import send_request
import json

def create_new_application(create_loan_application_request_schema : loan_application_schema.CreateLoanApplicationRequestSchema, 
                           db: Session):
    
    # validate business exists 
    business_in_db = business_dao.find_by_business_uuid(create_loan_application_request_schema.business_uuid, db)
    if(business_in_db == None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND ,
            detail="Business with this uuid not found"
        )
    
    loan_application_db_request = db_model.LoanApplication(
        business_uuid = create_loan_application_request_schema.business_uuid
    )
    loan_application_db_response = loan_application_dao.save(loan_application_db_request, db)
    return loan_application_schema.CreateLoanApplicationResponseSchema(
        business_uuid=loan_application_db_response.business_uuid,
        application_uuid=loan_application_db_response.application_uuid
    )

def update_application(update_loan_application_request_schema : loan_application_schema.UpdateLoanApplicationRequestSchema, 
                       db: Session):
    # verify if application exists 
    application_in_db = loan_application_dao.find_by_application_uuid(update_loan_application_request_schema.application_uuid, db)
    if(application_in_db == None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND ,
            detail="Application with this uuid not found"
        )
    
    if(update_loan_application_request_schema.accounting_provider_name != None):
        application_in_db.accounting_provider_name = update_loan_application_request_schema.accounting_provider_name.value 
    
    if(update_loan_application_request_schema.loan_amount != None):
        application_in_db.loan_amount_requested = update_loan_application_request_schema.loan_amount 
        
    loan_application_db_response = loan_application_dao.save(application_in_db, db)
    
    return loan_application_schema.UpdateLoanApplicationResponseSchema(
        application_uuid=loan_application_db_response.application_uuid,
        business_uuid=loan_application_db_response.business_uuid,
        loan_amount=loan_application_db_response.loan_amount_requested,
        application_status=loan_application_db_response.application_status,
        accounting_provider_name = loan_application_db_response.accounting_provider_name
    )

    
     
    

def submit_application(submit_loan_application_request_schema : loan_application_schema.SubmitLoanApplicationRequestSchema, 
                       db: Session):
    # verify if application exists
    application_in_db = loan_application_dao.find_by_application_uuid(submit_loan_application_request_schema.application_uuid, db)
    if(application_in_db == None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND ,
            detail="Application with this uuid not found"
        )
        
    if(application_in_db.accounting_balance_sheet_json == None):
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED ,
            detail="Balance Sheet Not found. Not allowed to submit before fetching the balance sheet."
        )

    business_in_db = business_dao.find_by_business_uuid(application_in_db.business_uuid, db)
    
    
    application_in_db.application_status = LoanApplicationStatus.SUBMITTED.value
    loan_application_db = loan_application_dao.save(application_in_db, db)
    
    # get preassessment value application 
    try:
        loan_application_db.pre_assessment_value, total_profit = loan_application_utils.get_preassessment_score(
            application_in_db.accounting_balance_sheet_json, 
            application_in_db.loan_amount_requested
        )
        application_in_db = loan_application_dao.save(application_in_db, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = str(e)
        )
        
    # get the decision 
    decision_service_response = send_request(
        RequestType.POST.value, 
        "https://apimocha.com/demyst/decision-service", 
        1000, headers=None, body= {
            "business_details": {
                "name": business_in_db.name,
                "year_established": business_in_db.year_of_establishment,
                "last_year_profit": total_profit
            },
            "pre_assessment_value": application_in_db.pre_assessment_value
        })
    
    application_in_db.decision_json = decision_service_response
    application_in_db.application_status = LoanApplicationStatus.LOAN_DECISION_COMPLETE.value 
    if(decision_service_response["loan_sanction"]==True):
        application_in_db.amount_sanctioned = int(application_in_db.loan_amount_requested * (application_in_db.pre_assessment_value /100))
    loan_application_dao.save(application_in_db, db)
    
    return loan_application_schema.SubmitLoanApplicationResponseSchema(
        application_uuid=application_in_db.application_uuid,
        business_uuid=application_in_db.business_uuid,
        loan_amount=application_in_db.loan_amount_requested,
        application_status=application_in_db.application_status,
        accounting_provider_name = application_in_db.accounting_provider_name,
        decision=application_in_db.decision_json,
        pre_assessment_value= application_in_db.pre_assessment_value,
        loan_amount_sanctioned=application_in_db.amount_sanctioned
    )