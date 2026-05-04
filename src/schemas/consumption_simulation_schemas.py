from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict

class SimulationSchema(BaseModel):
    description: Optional[str] = None
    starting_date: date
    ending_date: date
    si_measurement_unit: str
    value: Decimal



class UpdateSimulationSchema(BaseModel):
    new_description: Optional[str] = None
    new_starting_date: Optional[date] = None
    new_ending_date: Optional[date] = None
    new_si_measurement_unit: Optional[str] = None
    new_value: Optional[Decimal] = None
    


class ResponseSimulationSchema(BaseModel):
    # SQLAlchemy retorna Sequence[ConsumptionSimulation], que é uma lista de todos os objetos de simulação encontrados
    # Isso aqui permite que o Pydantic automaticamente pegue os dados retirados de uma lista de objetos e transforme em JSON
    # Basicamente ele cria um JSON completo para cada elemento da lista de objetos que o SQLAlchemy retorna
    model_config = (ConfigDict(from_attributes=True))
    
    id: int
    description: str
    starting_date: date
    ending_date: date
    si_measurement_unit: str
    value: Decimal
    
    

class QuerySimulationSchema(BaseModel):
    measurement_unit: Optional[str] = None
    starting_date: Optional[date] = None
    ending_date: Optional[date] = None
    minimum_value: Optional[Decimal] = None
    maximum_value: Optional[Decimal] = None