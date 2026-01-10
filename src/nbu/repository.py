from .api import Client
from .responses import ExchangeRate
from .requests_models import ExchangeRateRequest

class Repository:
    def __init__(self, client=None):
        #TODO:move url to env or config
        self._client = client or Client('https://bank.gov.ua')
    
    def get_rates(self, date):
        request = ExchangeRateRequest(date)
        raw_data = self._client.send(request)
        
        validated = [ExchangeRate(**item).model_dump() for item in raw_data]
        return validated
