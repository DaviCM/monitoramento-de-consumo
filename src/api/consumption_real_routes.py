from fastapi import APIRouter, Depends, HTTPException
from src.models.user_model import User
from src.schemas.consumption_real_schemas import ConsumptionSchema, UpdateConsumptionSchema
from src.controllers.consumption_history_controller import create_consumption, get_user_consumption_history, edit_consumption, delete_consumption
from src.errors.consumption_errors import ConsumptionsNotFoundError, InvalidDateError, InvalidConsumptionValueError
from src.errors.user_errors import UserNotFoundError
from src.api.security import get_current_user

consumption_real_router = APIRouter(prefix="/consumption_real", tags=["consumo_real"])

@consumption_real_router.post("/criar_consumo_real")
async def create_consumption_real(consumo_real_schema: ConsumptionSchema, current_user: User = Depends(get_current_user)):
    try:
        create_consumption(
            current_user=current_user,
            new_starting_date=consumo_real_schema.starting_date,
            new_ending_date=consumo_real_schema.ending_date,
            new_si_measurement_unit=consumo_real_schema.si_measurement_unit,
            new_value=consumo_real_schema.value
        )
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except InvalidDateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except InvalidConsumptionValueError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return {"mensagem": "dados de consumo cadastrado com sucesso"}


@consumption_real_router.get("/listar_consumo_real")
async def list_consumption_real(current_user: User = Depends(get_current_user)):
    try:
        consumption = get_user_consumption_history(current_user)
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except ConsumptionsNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return {"mensagem": consumption}


@consumption_real_router.put("/editar_consumo_real")
async def change_consumption(consumo_real_schema: UpdateConsumptionSchema, current_user: User = Depends(get_current_user)):
    try:
        edit_consumption(
            current_user=current_user,
            target_consumption=consumo_real_schema.id,
            new_starting_date=consumo_real_schema.new_starting_date,
            new_ending_date=consumo_real_schema.new_ending_date,
            new_measurement_unit=consumo_real_schema.new_si_measurement_unit,
            new_value=consumo_real_schema.new_value
        )
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except ConsumptionsNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except InvalidDateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except InvalidConsumptionValueError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return {"mensagem": "Registros de consumos alterados com sucesso"}


@consumption_real_router.delete("/deletar_consumo/{id}")
async def delete_consumption_route(id: int, current_user: User = Depends(get_current_user)):
    try:
        consumption = get_user_consumption_history(current_user)
        delete_consumption(current_user, consumption)
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except ConsumptionsNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return {"mensagem": "consumo excluído com sucesso"}




