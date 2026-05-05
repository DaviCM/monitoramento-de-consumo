from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from src.models.consumption_history_model import ConsumptionHistory
from src.models.user_model import User
from src.schemas.consumption_real_schemas import ConsumptionSchema, UpdateConsumptionSchema, QueryConsumptionSchema
from src.errors.consumption_errors import *
from src.errors.user_errors import UserNotFoundError
from src.database.session import get_session

# Irá causar um erro caso um user tente editar um consumo que não é dele!
def get_owned_consumption(session: Session, current_user: User, target_consumption_id: int):
    stmt = select(ConsumptionHistory).where(
            and_(ConsumptionHistory.creator_id == current_user.id,
                ConsumptionHistory.id == target_consumption_id))
    
    result = session.scalar(stmt)
        
    if result == None:
        raise ConsumptionsNotFoundError
        
    return result


def create_consumption(current_user: User, params: ConsumptionSchema):
    if current_user == None:
        raise UserNotFoundError
    
    if params.starting_date == None:
        raise InvalidDateError
    
    if (params.ending_date != None) and (params.starting_date > params.ending_date):
        raise InvalidDateError
    
    if params.value <= 0:
        raise InvalidConsumptionValueError
    
    new_consumption = ConsumptionHistory(**(params.model_dump(exclude_none=True)), creator_id=current_user.id)
    
    with get_session() as session:
        session.add(new_consumption)
        session.flush()
        
    return new_consumption

# Ideia muito eficiente da IA e do GitHub issues no SQLAlchemy
# Criar apenas uma função de query, e utilizar os parâmetros conforme eles forem requisitados
# Todos são opcionais, e a query é montada dinamicamente a partir de quais foram preenchidos
# Implementar em user e nos consumos
# Ideia: type hint |, para identificar o tipo ou None, como no pydantic

def get_user_consumption_history(current_user: User, params: QueryConsumptionSchema):
    if current_user == None:
        raise UserNotFoundError
    
    if (params.maximum_value != None) and (params.minimum_value != None):
        if params.minimum_value > params.maximum_value:
            raise InvalidConsumptionValueError
    
    if (params.ending_date != None) and (params.starting_date != None):
        if params.starting_date > params.ending_date:
            raise InvalidDateError

    stmt = select(ConsumptionHistory).where(ConsumptionHistory.creator_id == current_user.id)
    
    if params.measurement_unit != None:
        stmt = stmt.where(ConsumptionHistory.si_measurement_unit == (params.measurement_unit.lower()).strip())
    
    # comparação por igualdade ou maioridade, pois quero datas depois da data de início
    if params.starting_date != None:
        stmt = stmt.where(ConsumptionHistory.starting_date >= params.starting_date)
        
    if params.ending_date != None:
        stmt = stmt.where(ConsumptionHistory.ending_date <= params.ending_date)
        
    if params.minimum_value != None:
        stmt = stmt.where(ConsumptionHistory.value >= params.minimum_value)
        
    if params.maximum_value != None:
        stmt = stmt.where(ConsumptionHistory.value <= params.maximum_value)
    
    # All já trata os scalars como objetos separados, pois ele os consome inteiros
    with get_session() as session:
        consumptions = session.scalars(stmt).all()
        
        if consumptions == []:
            raise ConsumptionsNotFoundError
        
    return consumptions


def edit_consumption(current_user: User, target_consumption_id: int, params: UpdateConsumptionSchema):
    if current_user == None:
        raise UserNotFoundError
    
    if (params.new_value != None) and (params.new_value <= 0):
        raise InvalidConsumptionValueError
    
    with get_session() as session:
        to_edit = get_owned_consumption(session, current_user, target_consumption_id)

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


def delete_consumption(current_user: User, target_consumption_id: int):
    if current_user == None:
        raise UserNotFoundError
    
    with get_session() as session:
        to_delete = get_owned_consumption(session, current_user, target_consumption_id)
        session.delete(to_delete)
        
