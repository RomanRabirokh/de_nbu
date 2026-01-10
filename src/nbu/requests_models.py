class Request:
    method = 'GET'
    path = '/'

    def __init__(self, format='json'):
        self.format = format
    
    def get_payload(self):
        return {"format": self.format}

class ExchangeRateRequest(Request):
    path = '/NBU_Exchange/exchange'

    def __init__(self, date):
        super().__init__()
        self.date = date

    def get_payload(self):
        payload = super().get_payload()
        payload.update({"date": self.date})

        if self.format == 'json':
            payload.update({"json": ""})
        return payload
