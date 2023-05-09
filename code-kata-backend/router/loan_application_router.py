from fastapi import APIRouter, Depends
from db_config.db import get_db
from sqlalchemy.orm import Session

from schema import loan_application_schema
from service import loan_application_service

router = APIRouter(
    prefix="/api/v1/loan/application",
    tags=["application"]
)


@router.post("/new")
async def create_new_application(create_loan_application_request_schema : loan_application_schema.CreateLoanApplicationRequestSchema, 
                                 db: Session = Depends(get_db)):
    return loan_application_service.create_new_application(create_loan_application_request_schema, db)

@router.post("/update")
async def update_application(update_loan_application_request_schema : loan_application_schema.UpdateLoanApplicationRequestSchema, 
                            db: Session = Depends(get_db)):
    return loan_application_service.update_application(update_loan_application_request_schema, db)

@router.post("/submit")
async def submit_application(submit_loan_application_request_schema : loan_application_schema.SubmitLoanApplicationRequestSchema, 
                             db: Session = Depends(get_db)):
    return loan_application_service.submit_application(submit_loan_application_request_schema, db)


