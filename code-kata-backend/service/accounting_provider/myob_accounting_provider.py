
from constants.accounting_provider_enum import AccountingProviderEnum
from constants.request_enum import RequestType
import requests
from service.accounting_provider.base_accounting_provider import BaseAccountingProvider

from utils.common_utils import send_request


class MyobAccountingProvider(BaseAccountingProvider):
    def name(self):
        return AccountingProviderEnum.MYOB
    
    def extract_accounting_balance_sheet(self):
        return send_request(RequestType.GET.value, 'https://apimocha.com/demyst/myob/accounting-service', 1000 )