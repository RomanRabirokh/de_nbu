from datetime import date, datetime
from pydantic import BaseModel, Field, field_validator

class ExchangeRate(BaseModel):
    TimeSign: str
    StartDate: date
    Units: int
    CurrencyCode: str
    CurrencyCodeL: str = Field(min_length=3, max_length=3)
    Amount: float

    @field_validator('StartDate', mode='before')
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%d.%m.%Y").date()
        return value
