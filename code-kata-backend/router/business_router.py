from fastapi import APIRouter, Depends
from db_config.db import get_db
from sqlalchemy.orm import Session


from schema import business_schema
from service import business_service

router = APIRouter(
    prefix="/api/v1/loan/business",
    tags=["business"]
)


@router.post("/register")
async def business_register(business_regsiter_schema : business_schema.BusinessRegisterRequestSchema, db: Session = Depends(get_db)):
    return business_service.regsiter_business(business_regsiter_schema, db)


@router.post("/search")
async def find_business(business_request_schema : business_schema.FindBusinessRequestSchema, db: Session = Depends(get_db)):
    return business_service.find_business(business_request_schema, db)
