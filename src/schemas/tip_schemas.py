from pydantic import BaseModel, ConfigDict

class ResponseTipSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    si_measurement_unit: str
    tip: str