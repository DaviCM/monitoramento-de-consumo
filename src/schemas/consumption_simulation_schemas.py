from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Consumo_Simulation_Schema(BaseModel):
    starting_date: datetime
    ending_date:  datetime
    value: float
    si_measurement_unit:  int

class Consumption_Simulation_UpdateSchema(BaseModel):
    new_starting_date: Optional[datetime] = None
    new_ending_date: Optional[datetime] = None
    new_si_measurement_unit: Optional[str] = None
    new_value: Optional[float] = None