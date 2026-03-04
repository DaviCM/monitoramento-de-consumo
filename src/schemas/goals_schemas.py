from pydantic import BaseModel
from datetime import datetime

class GoalsSchema(BaseModel):
    starting_date: str
    ending_date: str
    si_measurement_unit:  str
    value: str