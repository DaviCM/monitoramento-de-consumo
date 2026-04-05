from fastapi import APIRouter, Depends, HTTPException
from src.models.user_model import User
from src.schemas.goals_schemas import GoalsSchema, UpdateGoalsSchema
from src.controllers.goal_controller import create_simulation, get_user_simulations, edit_simulation, delete_simulation
from src.errors.consumption_errors import ConsumptionsNotFoundError, InvalidDateError, InvalidConsumptionValueError
from src.errors.user_errors import UserNotFoundError
from src.api.security import get_current_user

goals_router = APIRouter(prefix="/goals", tags=["metas"])

@goals_router.post("/criar_metas")
async def create_goals(goals_schema: GoalsSchema, current_user: User = Depends(get_current_user)):
    try:
        create_simulation(
            current_user=current_user,
            new_starting_date=goals_schema.starting_date,
            new_ending_date=goals_schema.ending_date,
            new_si_measurement_unit=goals_schema.si_measurement_unit,
            new_value=goals_schema.value
        )
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except InvalidDateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except InvalidConsumptionValueError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return {"mensagem": "Meta cadastrada com sucesso"}


@goals_router.get("/listar_metas")
async def list_goals(current_user: User = Depends(get_current_user)):
    try:
        goals_list = get_user_simulations(current_user)
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except ConsumptionsNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return {"mensagem": goals_list}


@goals_router.put("/editar_meta_de_consumo")
async def change_goal(goals_schema: UpdateGoalsSchema, current_user: User = Depends(get_current_user)):
    try:
        edit_simulation(
            current_user=current_user,
            target_simulation=goals_schema.id,
            new_starting_date=goals_schema.new_starting_date,
            new_ending_date=goals_schema.new_ending_date,
            new_measurement_unit=goals_schema.new_si_measurement_unit,
            new_value=goals_schema.new_value
        )
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except ConsumptionsNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except InvalidDateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except InvalidConsumptionValueError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return {"mensagem": "Meta alterada com sucesso"}


@goals_router.delete("/deletar_meta/{id}")
async def delete_goals(id: int, current_user: User = Depends(get_current_user)):
    try:
        delete_simulation(current_user, id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except ConsumptionsNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return {"mensagem": "Meta excluída com sucesso"}    

