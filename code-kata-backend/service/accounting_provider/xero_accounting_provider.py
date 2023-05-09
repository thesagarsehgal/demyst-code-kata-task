
from constants.accounting_provider_enum import AccountingProviderEnum
import requests
from constants.request_enum import RequestType

from service.accounting_provider.base_accounting_provider import BaseAccountingProvider
from utils.common_utils import send_request


class XeroAccountingProvider(BaseAccountingProvider):
    def name(self):
        return AccountingProviderEnum.XERO
    
    def extract_accounting_balance_sheet(self):
        return send_request(RequestType.GET.value, 'https://apimocha.com/demyst/xero/accounting-service', 1000 )

            