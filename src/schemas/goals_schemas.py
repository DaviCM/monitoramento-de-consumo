from pydantic import BaseModel
from datetime import date
from decimal import Decimal
from typing import Optional

class GoalSchema(BaseModel):
    id: int
    starting_date: date
    ending_date: date
    si_measurement_unit: str
    value: Decimal



class UpdateGoalSchema(BaseModel):
    id: int
    new_starting_date: Optional[date] = None
    new_ending_date: Optional[date] = None
    new_si_measurement_unit: Optional[str] = None
    new_value: Optional[Decimal] = None
    
    