from fastapi import APIRouter, Depends, HTTPException, status

from src.models.user_model import User
from src.controllers.consumption_history_controller import *
from src.schemas.consumption_real_schemas import *
from src.errors.consumption_errors import *
from src.errors.user_errors import UserNotFoundError
from src.auth.access_token_auth import get_current_user

consumption_real_router = APIRouter(prefix="/api/consumos", tags=["Consumos Reais"])

@consumption_real_router.post(path="/criar_consumo", status_code=status.HTTP_201_CREATED, response_model=ResponseConsumptionSchema)
async def create_consumption_route(to_create: ConsumptionSchema, current_user: User = Depends(get_current_user)):
    try:
        return create_consumption(current_user=current_user, params=to_create)
    
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except InvalidDateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except InvalidConsumptionValueError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)



@consumption_real_router.post(path="/listar_consumos", status_code=status.HTTP_200_OK, response_model=list[ResponseConsumptionSchema])
async def list_consumption_route(params: QueryConsumptionSchema, current_user: User = Depends(get_current_user)):
    try:
        return get_user_consumption_history(current_user=current_user, params=params)
        
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
        
    except ConsumptionsNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except InvalidConsumptionValueError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
        
    except InvalidDateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)



@consumption_real_router.patch(path="/editar_consumo/{id}", status_code=status.HTTP_200_OK, response_model=ResponseConsumptionSchema)
async def edit_consumption_route(id: int, params: UpdateConsumptionSchema, current_user: User = Depends(get_current_user)):
    try:
        return edit_consumption(current_user=current_user, target_consumption_id=id, params=params)
        
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except ConsumptionsNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except InvalidConsumptionValueError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except InvalidDateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)



@consumption_real_router.delete(path="/deletar_consumo/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_consumption_route(id: int, current_user: User = Depends(get_current_user)):
    try:
        delete_consumption(current_user=current_user, 
                           target_consumption_id=id
                           )
        
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except ConsumptionsNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    


