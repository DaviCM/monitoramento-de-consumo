from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict

class GoalSchema(BaseModel):
    description: Optional[str] = None
    starting_date: date
    ending_date: date
    si_measurement_unit: str
    value: Decimal



class UpdateGoalSchema(BaseModel):
    new_description: Optional[str] = None
    new_starting_date: Optional[date] = None
    new_ending_date: Optional[date] = None
    new_si_measurement_unit: Optional[str] = None
    new_value: Optional[Decimal] = None



class ResponseGoalSchema(BaseModel):
    model_config = (ConfigDict(from_attributes=True))
    
    id: int
    description: str
    starting_date: date
    ending_date: date
    si_measurement_unit: str
    value: Decimal
    
    

class QueryGoalSchema(BaseModel):
    measurement_unit: Optional[str] = None
    starting_date: Optional[date] = None
    ending_date: Optional[date] = None
    minimum_value: Optional[Decimal] = None
    maximum_value: Optional[Decimal] = None