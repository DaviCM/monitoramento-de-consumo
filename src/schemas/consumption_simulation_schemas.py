from pydantic import BaseModel, ConfigDict
from datetime import date
from decimal import Decimal
from typing import Optional

class SimulationSchema(BaseModel):
    starting_date: date
    ending_date: date
    si_measurement_unit: str
    value: Decimal



class UpdateSimulationSchema(BaseModel):
    id: int
    new_starting_date: Optional[date]
    new_ending_date: Optional[date]
    new_si_measurement_unit: Optional[str]
    new_value: Optional[Decimal]
    


class ResponseSimulationSchema(BaseModel):
    # SQLAlchemy retorna Sequence[ConsumptionSimulation], que é uma lista de todos os objetos de simulação encontrados
    # Isso aqui permite que o Pydantic automaticamente pegue os dados retirados de uma lista de objetos e transforme em JSON
    # Basicamente ele cria um JSON completo para cada elemento da lista de objetos que o SQLAlchemy retorna
    model_config = (ConfigDict(from_attributes=True))
    
    id: int
    starting_date: date
    ending_date: date
    measurement_unit: str
    value: Decimal
    
    

class QuerySimulationSchema(BaseModel):
    measurement_unit: Optional[str]
    starting_date: Optional[date]
    ending_date: Optional[date]
    minimum_value: Optional[Decimal]
    maximum_value: Optional[Decimal]