from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from src.models.goal_model import Goal
from src.models.user_model import User
from src.schemas.goals_schemas import GoalSchema, UpdateGoalSchema, QueryGoalSchema
from src.errors.consumption_errors import *
from src.errors.user_errors import UserNotFoundError
from src.database.session import get_session

# Irá causar um erro caso um user tente editar um consumo que não é dele!
def get_owned_goals(session: Session, current_user: User, target_goal_id: int):
    stmt = select(Goal).where(
            and_(Goal.creator_id == current_user.id,
                Goal.id == target_goal_id))

    result = session.scalar(stmt)
    
    if result == None:
        raise ConsumptionsNotFoundError
        
    return result


def create_goal(current_user: User, params: GoalSchema):
    if current_user == None:
        raise UserNotFoundError
    
    if (params.starting_date == None) or (params.starting_date > params.ending_date):
        raise InvalidDateError
    
    if params.value <= 0:
        raise InvalidConsumptionValueError
    
    new_goal = Goal(**(params.model_dump(exclude_none=True)))
    
    with get_session() as session:
        session.add(new_goal)
        session.flush()
        
    return new_goal
    
    
def get_user_goals(current_user: User, params: QueryGoalSchema):
    if current_user == None:
        raise UserNotFoundError
    
    if (params.maximum_value != None) and (params.minimum_value != None):
        if params.minimum_value > params.maximum_value:
            raise InvalidConsumptionValueError
    
    if (params.ending_date != None) and (params.starting_date != None):
        if params.starting_date > params.ending_date:
            raise InvalidDateError

    stmt = select(Goal).where(Goal.creator_id == current_user.id)
    
    if params.measurement_unit != None:
        stmt = stmt.where(Goal.si_measurement_unit == (params.measurement_unit.lower()).strip())
    
    # comparação por igualdade ou maioridade, pois quero datas depois da data de início
    if params.starting_date != None:
        stmt = stmt.where(Goal.starting_date >= params.starting_date)
        
    if params.ending_date != None:
        stmt = stmt.where(Goal.ending_date <= params.ending_date)
        
    if params.value != None:
        stmt = stmt.where(Goal.value >= params.minimum_value)
        
    if params.maximum_value != None:
        stmt = stmt.where(Goal.value <= params.maximum_value)
    
    # All já trata os scalars como objetos separados, pois ele os consome inteiros
    with get_session() as session:
        goals = session.scalars(stmt).all()
        
        if goals == []:
            raise ConsumptionsNotFoundError
        
    return goals


def edit_goal(current_user: User, target_goal_id: int, params: UpdateGoalSchema):
    if current_user == None:
        raise UserNotFoundError
    
    if (params.new_value != None) and (params.new_value <= 0):
        raise InvalidConsumptionValueError
    
    with get_session() as session:
        to_edit = get_owned_goals(session, current_user, target_goal_id)

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


def delete_goal(current_user: User, target_goal_id: int):
    if current_user == None:
        raise UserNotFoundError
    
    with get_session() as session:
        to_delete = get_owned_goals(session, current_user, target_goal_id)
        session.delete(to_delete)
        
