from pydantic import BaseModel, Field

from constants.accounting_provider_enum import AccountingProviderEnum


class AccountingProvider(BaseModel):
    accounting_provider_name: str
    
class BalanceSheetMonthlyData(BaseModel):
    year: int 
    month: int 
    profitOrLoss: int
    assetsValue: int 
    
# request schema 

# class AllAccountingProviderRequestSchema(BaseModel):
#     pass

class GetBalanceSheetRequestSchema(BaseModel):
    application_uuid: str

    
# response schema 

class AllAccountingProviderResponseSchema(BaseModel):
    all_providers: list[AccountingProvider]

class GetBalanceSheetResponseSchema(BaseModel):
    application_uuid: str
    balance_sheet_extracted: bool
    balance_sheet_data: list[BalanceSheetMonthlyData]
