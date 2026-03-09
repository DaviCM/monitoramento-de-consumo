from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional

class GoalsSchema(BaseModel):
    starting_date: datetime
    ending_date: datetime
    si_measurement_unit:  str
    value: Decimal
    id: int

class UpdateGoalsSchema(BaseModel):
    new_starting_date: Optional[datetime] = None
    id: int
    new_ending_date: Optional[datetime] = None
    new_si_measurement_unit: Optional[str] = None
    new_value: Optional[Decimal] = None

