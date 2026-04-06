from fastapi import APIRouter, Depends, HTTPException, status
from src.models.user_model import User
from src.controllers.consumption_history_controller import *
from src.schemas.consumption_real_schemas import *
from src.errors.consumption_errors import *
from src.errors.user_errors import UserNotFoundError
from src.api.security import get_current_user

consumption_real_router = APIRouter(prefix="/consumos", tags=["consumos"])

@consumption_real_router.post(prefix="/criar_consumo", status_code=status.HTTP_201_CREATED, response_model=ResponseConsumptionSchema)
async def create_consumption_route(consumo_real_schema: ConsumptionSchema, current_user: User = Depends(get_current_user)):
    try:
        return create_consumption(current_user=current_user,
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



@consumption_real_router.get(prefix="/listar_consumos", status_code=status.HTTP_200_OK, response_model=list[ResponseConsumptionSchema])
async def list_consumption_route(params: QueryConsumptionSchema, current_user: User = Depends(get_current_user)):
    try:
        return get_user_consumption_history(current_user=current_user,
                                            target_measurement_unit=params.measurement_unit, 
                                            target_starting_date=params.starting_date,
                                            target_ending_date=params.ending_date,
                                            minimum_value=params.minimum_value, 
                                            maximum_value=params.maximum_value,
                                            )
        
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
        
    except ConsumptionsNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except InvalidConsumptionValueError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
        
    except InvalidDateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)



@consumption_real_router.patch(prefix="/editar_consumo/{id}", status_code=status.HTTP_200_OK, response_model=ResponseConsumptionSchema)
async def edit_consumption_route(id: int, params: UpdateConsumptionSchema, current_user: User = Depends(get_current_user)):
    try:
        return edit_consumption(current_user=current_user,
                                target_consumption=id,
                                new_starting_date=params.new_starting_date,
                                new_ending_date=params.new_ending_date,
                                new_measurement_unit=params.new_si_measurement_unit,
                                new_value=params.new_value
                                )
        
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except ConsumptionsNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except InvalidConsumptionValueError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except InvalidDateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)



@consumption_real_router.delete(prefix="/deletar_consumo/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_consumption_route(id: int, current_user: User = Depends(get_current_user)):
    try:
        delete_consumption(current_user=current_user, 
                           target_consumption_id=id
                           )
        
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except ConsumptionsNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    


