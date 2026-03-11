from fastapi import APIRouter, Depends, HTTPException # importar do fast api o roteador
from src.models.consumption_simulation_model import ConsumptionSimulation
from src.database.session import get_session
from src.schemas.consumption_simulation_schemas import Consumo_Simulation_Schema, Consumption_Simulation_UpdateSchema


consumption_simulation_router = APIRouter(prefix= "/consumption_simulation", tags= ["consumo_simulado"])


@consumption_simulation_router.post("/criar_simulação_de_consumo")
async def create_consumption_real(consumo_simulado_schema: Consumo_Simulation_Schema, session = Depends(get_session)):
     new_consumption = ConsumptionSimulation(
    starting_date=consumo_simulado_schema.starting_date,
    ending_date=consumo_simulado_schema.ending_date,
    si_measurement_unit=consumo_simulado_schema.si_measurement_unit,
    value=consumo_simulado_schema.value
)
     session.add(new_consumption)
     return{"mensagem": "simulação de consumo cadastrada com sucesso"}


@consumption_simulation_router.get("/listar_consumo_real")
async def list_consumption_real(session = Depends(get_session)):
    consumption_simu = session.query(ConsumptionSimulation).all()
    if not consumption_simu:
        raise HTTPException(status_code=404, detail="Lista de simulação de consumo não encontrada")
    else:
        return{"mensagem": consumption_simu }


@consumption_simulation_router.put("/editar_simulação_de_consumo")
async def change_consumption(consumo_simulado_schema: Consumption_Simulation_UpdateSchema, session = Depends(get_session)):
    consumption = session.query(ConsumptionSimulation).filter(ConsumptionSimulation.id == consumo_simulado_schema.id).first()
    if not consumption:
        raise HTTPException(status_code=404, detail = "Registros de consumo não encontrado")
    
    if consumo_simulado_schema.new_starting_date is not None:
            consumption.starting_date = consumo_simulado_schema.new_starting_date
            
    if consumo_simulado_schema.new_ending_date is not None:
            consumption.ending_date = consumo_simulado_schema.new_ending_date
            
    if consumo_simulado_schema.new_si_measurement_unit is not None:
            consumption.si_measurement_unit = consumo_simulado_schema.new_si_measurement_unit
            
    if consumo_simulado_schema.new_value is not None:
            consumption.value = consumo_simulado_schema.new_value

    return{"mensagem" : "Simulação de consumos alterados com sucesso"}


@consumption_simulation_router.delete("/deletar_consumo/{id}")
async def delete_consumption(id: int, session = Depends(get_session)):
    consumption = session.query(ConsumptionSimulation).filter(ConsumptionSimulation. id == id).first()
    if not consumption:
        raise HTTPException(status_code=404, detail=" Simulação de consumo não encontrado")
    else:
        session.delete(consumption)
        return {"mensagem": "simulação de consumo excluído com sucesso  "}
    

