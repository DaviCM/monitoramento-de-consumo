from fastapi import APIRouter, Depends, HTTPException, status # importar do fast api o roteador
from src.controllers.consumption_simulations_controller import *
from src.schemas.consumption_simulation_schemas import *
from src.api.security import get_current_user

consumption_simulation_router = APIRouter(prefix= "/simulacoes", tags=["Simulações"])

@consumption_simulation_router.post(prefix="/criar_simulacao", status_code=status.HTTP_201_CREATED, response_model=ResponseSimulationSchema)
async def create_simulation_route(to_create: SimulationSchema, current_user: User = Depends(get_current_user)):
    try:
        return create_simulation(current_user=current_user,
                                 starting_date=to_create.starting_date,
                                 ending_date=to_create.ending_date,
                                 si_measurement_unit=to_create.si_measurement_unit,
                                 value=to_create.value
                                 )
        
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except InvalidDateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except InvalidConsumptionValueError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)



# Essa função está retornando uma lista das respostas que são geradas automaticamente pelo Pydantic
# Controller irá retornar uma lista de objetos de simulação, e o pydantic tratará com base no response_model
# Para mostrar já formatado em JSON
@consumption_simulation_router.get(prefix="/listar_simulacoes", status_code=status.HTTP_200_OK, response_model=list[ResponseSimulationSchema])
async def list_simulations_route(params: QuerySimulationSchema, current_user: User = Depends(get_current_user)):
    try:
        return get_user_simulations(current_user=current_user,
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
    


@consumption_simulation_router.patch(prefix="/editar_simulacao/{id}", status_code=status.HTTP_200_OK, response_model=ResponseSimulationSchema)
async def edit_simulation_route(id: int, params: UpdateSimulationSchema, current_user: User = Depends(get_current_user)):
    try:
        return edit_simulation(current_user=current_user,
                               target_simulation_id=id,
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
    


@consumption_simulation_router.delete(prefix="/deletar_simulacao/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_simulation_route(id: int, current_user: User = Depends(get_current_user)):
    try:
        delete_simulation(current_user=current_user,
                          target_consumption_id=id)
    
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except ConsumptionsNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    

