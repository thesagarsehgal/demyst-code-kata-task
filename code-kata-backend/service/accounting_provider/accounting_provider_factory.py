from constants.accounting_provider_enum import AccountingProviderEnum
from service.accounting_provider.myob_accounting_provider import MyobAccountingProvider
from service.accounting_provider.xero_accounting_provider import XeroAccountingProvider


class AccountingProviderFactory:
    def get(self, accounting_provider_name):
        if(accounting_provider_name==AccountingProviderEnum.XERO.value):
            return XeroAccountingProvider()
        elif(accounting_provider_name==AccountingProviderEnum.MYOB.value):
            return MyobAccountingProvider()