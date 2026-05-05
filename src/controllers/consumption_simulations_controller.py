from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from src.models.consumption_simulation_model import ConsumptionSimulation
from src.models.user_model import User
from src.schemas.consumption_simulation_schemas import SimulationSchema, UpdateSimulationSchema, QuerySimulationSchema
from src.errors.consumption_errors import *
from src.errors.user_errors import UserNotFoundError
from src.database.session import get_session

# Irá causar um erro caso um user tente editar um consumo que não é dele!
def get_owned_simulation(session: Session, current_user: User, target_simulation_id: int):
    stmt = select(ConsumptionSimulation).where(
            and_(ConsumptionSimulation.creator_id == current_user.id,
                ConsumptionSimulation.id == target_simulation_id))
    
    result = session.scalar(stmt)
        
    if result == None:
        raise ConsumptionsNotFoundError
        
    return result


def create_simulation(current_user: User, params: SimulationSchema):
    if current_user == None:
        raise UserNotFoundError
    
    if (params.starting_date == None) or (params.starting_date > params.ending_date):
        raise InvalidDateError
    
    if params.value <= 0:
        raise InvalidConsumptionValueError
    
    new_simulation = ConsumptionSimulation(**(params.model_dump(exclude_none=True)), creator_id=current_user.id)
    
    with get_session() as session:
        session.add(new_simulation)
        # gera o insert da simulação antes do commit, para podermos retornar ela completa
        session.flush()
        
    return new_simulation
    
    
def get_user_simulations(current_user: User, params: QuerySimulationSchema):
    if current_user == None:
        raise UserNotFoundError
    
    if (params.maximum_value != None) and (params.minimum_value != None):
        if params.minimum_value > params.maximum_value:
            raise InvalidConsumptionValueError
    
    if (params.ending_date != None) and (params.starting_date != None):
        if params.starting_date > params.ending_date:
            raise InvalidDateError

    stmt = select(ConsumptionSimulation).where(ConsumptionSimulation.creator_id == current_user.id)
    
    if params.measurement_unit != None:
        stmt = stmt.where(ConsumptionSimulation.si_measurement_unit == (params.measurement_unit.lower()).strip())
    
    # comparação por igualdade ou maioridade, pois quero datas depois da data de início
    if params.starting_date != None:
        stmt = stmt.where(ConsumptionSimulation.starting_date >= params.starting_date)
        
    if params.ending_date != None:
        stmt = stmt.where(ConsumptionSimulation.ending_date <= params.ending_date)
        
    if params.minimum_value != None:
        stmt = stmt.where(ConsumptionSimulation.value >= params.minimum_value)
        
    if params.maximum_value != None:
        stmt = stmt.where(ConsumptionSimulation.value <= params.maximum_value)
    
    # All já trata os scalars como objetos separados, pois ele os consome inteiros
    with get_session() as session:
        simulations = session.scalars(stmt).all()
        
        if simulations == []:
            raise ConsumptionsNotFoundError
        
    return simulations


def edit_simulation(current_user: User, target_simulation_id: int, params: UpdateSimulationSchema):
    
    if current_user == None:
        raise UserNotFoundError
    
    if (params.new_value != None) and (params.new_value <= 0):
        raise InvalidConsumptionValueError
        
    with get_session() as session:
        to_edit = get_owned_simulation(session, current_user, target_simulation_id)

        if (params.new_starting_date != None) and (params.new_starting_date > to_edit.ending_date):
            raise InvalidDateError

        if (params.new_ending_date != None) and (params.new_ending_date < to_edit.starting_date):
            raise InvalidDateError
    
        if params.new_starting_date != None:
            to_edit.starting_date = params.new_starting_date
            
        if params.new_ending_date != None:
            to_edit.ending_date = params.new_ending_date
            
        if params.new_si_measurement_unit != None:
            to_edit.si_measurement_unit = (params.new_si_measurement_unit.lower()).strip()
            
        if params.new_value != None:
            to_edit.value = params.new_value
        
    return to_edit


def delete_simulation(current_user: User, target_consumption_id: int):
    if current_user == None:
        raise UserNotFoundError
    
    with get_session() as session:
        to_delete = get_owned_simulation(session, current_user, target_consumption_id)
        session.delete(to_delete)
        
