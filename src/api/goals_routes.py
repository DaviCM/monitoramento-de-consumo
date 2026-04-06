from fastapi import APIRouter, Depends, HTTPException, status
from src.models.user_model import User
from src.controllers.goal_controller import *
from src.schemas.goals_schemas import *
from src.errors.consumption_errors import *
from src.errors.user_errors import UserNotFoundError
from src.api.security import get_current_user

goals_router = APIRouter(prefix="/goals", tags=["Metas de Consumo"])

@goals_router.post(path="/criar_meta", status_code=status.HTTP_201_CREATED, response_model=ResponseGoalSchema)
async def create_goal_route(to_create: GoalSchema, current_user: User = Depends(get_current_user)):
    try:
        return create_goal(current_user=current_user,
                           new_starting_date=to_create.starting_date,
                           new_ending_date=to_create.ending_date,
                           new_si_measurement_unit=to_create.si_measurement_unit,
                           new_value=to_create.value
                           )
        
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except InvalidDateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except InvalidConsumptionValueError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)



@goals_router.get(path="/listar_metas", status_code=status.HTTP_200_OK, response_model=list[ResponseGoalSchema])
async def list_goals_route(params: QueryGoalSchema, current_user: User = Depends(get_current_user)):
    try:
        return get_user_goals(current_user=current_user,
                              target_measurement_unit=params.measurement_unit,
                              target_starting_date=params.starting_date,
                              target_ending_date=params.ending_date,
                              minimum_value=params.minimum_value,
                              maximum_value=params.maximum_value
                              )
        
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
        
    except ConsumptionsNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except InvalidConsumptionValueError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
        
    except InvalidDateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    


@goals_router.patch(path="/editar_meta/{id}", status_code=status.HTTP_200_OK, response_model=ResponseGoalSchema)
async def edit_goal_route(id: int, params: UpdateGoalSchema, current_user: User = Depends(get_current_user)):
    try:
        return edit_goal(current_user=current_user,
                         target_simulation=id,
                         new_starting_date=params.new_starting_date,
                         new_ending_date=params.new_ending_date,
                         new_measurement_unit=params.new_si_measurement_unit,
                         new_value=params.new_value
                         )
        
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except ConsumptionsNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except InvalidDateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except InvalidConsumptionValueError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    


@goals_router.delete(path="/deletar_meta/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal_route(id: int, current_user: User = Depends(get_current_user)):
    try:
        delete_goal(current_user=current_user, 
                    target_goal_id=id
                    )
        
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except ConsumptionsNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

