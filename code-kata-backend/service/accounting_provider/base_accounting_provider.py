from abc import ABC, abstractmethod

class BaseAccountingProvider(ABC):
    
    @abstractmethod
    def name(self):
        pass
    
    @abstractmethod
    def extract_accounting_balance_sheet(self):
        pass
    