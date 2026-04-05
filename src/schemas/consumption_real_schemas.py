from pydantic import BaseModel, ConfigDict
from datetime import date
from decimal import Decimal
from typing import Optional

class ConsumptionSchema(BaseModel):
    starting_date: date
    ending_date: date
    si_measurement_unit: str
    value: Decimal



class UpdateConsumptionSchema(BaseModel):
    new_starting_date: Optional[date]
    new_ending_date: Optional[date]
    new_si_measurement_unit: Optional[str]
    new_value: Optional[Decimal]
    


class ResponseConsumptionSchema(BaseModel):
    model_config = (ConfigDict(from_attributes=True))
    
    id: int
    starting_date: date
    ending_date: date
    measurement_unit: str
    value: Decimal
    
    

class QueryConsumptionSchema(BaseModel):
    measurement_unit: Optional[str]
    starting_date: Optional[date]
    ending_date: Optional[date]
    minimum_value: Optional[Decimal]
    maximum_value: Optional[Decimal]