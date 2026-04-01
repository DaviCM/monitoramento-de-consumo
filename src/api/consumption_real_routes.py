from fastapi import APIRouter, Depends, HTTPException 
from src.models.consumption_history_model import ConsumptionHistory
from src.database.session import get_session
from src.schemas.consumption_real_schemas import Consumo_Schema, ConsumptionUpdateSchema
from src.controllers.consumption_history_controller import * 
from src.errors.consumption_errors import * 

consumption_real_router = APIRouter(prefix= "/consumption_real", tags= ["consumo_real"])

@consumption_real_router.post("/criar_consumo_real")
async def create_consumption_real(consumo_real_schema: Consumo_Schema):
 try:
      create_consumption(consumo_real_schema.starting_date, consumo_real_schema.ending_date, consumo_real_schema.si_measurement_unit, consumo_real_schema.value)
 except InvalidDateError as e:
      raise HTTPException(status_code=e.status_code, detail=e.message)

 except InvalidConsumptionValueError as e:
      raise HTTPException(status_code=e.status_code, detail=e.message)

 return{"mensagem": "dados de consumo cadastrado com sucesso"}


@consumption_real_router.get("/listar_consumo_real")
async def list_consumption_real(consumo_real_schema: Consumo_Schema):
 try:
    consumption=get_user_consumption_history(consumo_real_schema.starting_date, consumo_real_schema.ending_date, consumo_real_schema.si_measurement_unit, consumo_real_schema.value)

 except ConsumptionsNotFoundError as e:
    raise HTTPException(status_code=e.status_code, detail=e.message)
 
 return{"mensagem": consumption }


@consumption_real_router.put("/editar_consumo_real")
async def change_consumption(consumo_real_schema: ConsumptionUpdateSchema, session = Depends(get_session)):
    consumption = session.query(ConsumptionHistory).filter(ConsumptionHistory.id == consumo_real_schema.id).first()
    if not consumption:
        raise HTTPException(status_code=404, detail = "Registros de consumo não encontrado")
    
    if consumo_real_schema.new_starting_date is not None:
            consumption.starting_date = consumo_real_schema.new_starting_date
            
    if consumo_real_schema.new_ending_date is not None:
            consumption.ending_date = consumo_real_schema.new_ending_date
            
    if consumo_real_schema.new_si_measurement_unit is not None:
            consumption.si_measurement_unit = consumo_real_schema.new_si_measurement_unit
            
    if consumo_real_schema.new_value is not None:
            consumption.value = consumo_real_schema.new_value
            
    return{"mensagem" : "Registros de consumos alterados com sucesso"}


@consumption_real_router.delete("/deletar_consumo/{id}")
async def delete_consumption(id: int, session = Depends(get_session)):
    consumption = session.query(ConsumptionHistory).filter(ConsumptionHistory. id == id).first()
    if not consumption:
        raise HTTPException(status_code=404, detail="Registros de consumo não encontrado")
    else:
        session.delete(consumption)
        return {"mensagem": "usuário excluído com sucesso  "}
    

@user_router.delete("/excluir_usuario")
async def delete_user(user_schema: get_current_user):
  try:
    delete_self(user_schema,get_current_user)
  except UserNotFoundError as e:
    raise HTTPException(status_code=e.status_code, detail=e.message)
  return{"mensagem" : "usuário excluído com sucesso !"}



@consumption_real_router.delete("/deletar_consumo/{id}")
async def delete_consumption(consumo_real_schema: Consumo_Schema):
    try:
        delete_consumption





