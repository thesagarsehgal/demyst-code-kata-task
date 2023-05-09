from fastapi import APIRouter, Depends
from db_config.db import get_db
from sqlalchemy.orm import Session


from schema import accounting_schema
from service import accounting_service


router = APIRouter(
    prefix="/api/v1/loan/accounting",
    tags=["accounting"]
)


@router.get("/providers/all")
async def get_all_providers(db: Session = Depends(get_db)):
    return accounting_service.get_all_providers(db)


@router.post("/providers/regsiter")
async def register_providers(name:str, db: Session = Depends(get_db)):
    return accounting_service.register_providers(name, db)

@router.post("/balance-sheet")
async def get_balance_sheet(get_balance_sheet_request_schema: accounting_schema.GetBalanceSheetRequestSchema ,db: Session = Depends(get_db)):
    return accounting_service.get_balance_sheet(get_balance_sheet_request_schema, db)
