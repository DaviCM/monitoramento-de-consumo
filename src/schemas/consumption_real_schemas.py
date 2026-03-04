from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Consumo_Schema(BaseModel):
    starting_date: datetime
    ending_date:  datetime
    si_measurement_unit: str
    value: float

class ConsumptionUpdateSchema(BaseModel):
    new_starting_date: Optional[datetime] = None
    new_ending_date: Optional[datetime] = None
    new_si_measurement_unit: Optional[str] = None
    new_value: Optional[float] = None