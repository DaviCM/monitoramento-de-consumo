from src.models.goal_model import Goal
from src.models.user_model import User
from src.errors.consumption_errors import *
from src.errors.user_errors import UserNotFoundError
from src.database.session import get_session
from datetime import date
from typing import Optional
from decimal import Decimal
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

# Irá causar um erro caso um user tente editar um consumo que não é dele!
def get_owned_goals(session: Session, current_user: User, target_goal_id: int):
    stmt = select(Goal).where(
            and_(Goal.creator_id == current_user.id,
                Goal.id == target_goal_id))

    result = session.scalar(stmt)
    
    if result == None:
        raise ConsumptionsNotFoundError
        
    return result


def create_goal(current_user: User, new_starting_date: date, new_ending_date: date, new_si_measurement_unit: str, new_value: Decimal):
    if current_user == None:
        raise UserNotFoundError
    
    if (new_starting_date == None) or (new_starting_date > new_ending_date):
        raise InvalidDateError
    
    if new_value <= 0:
        raise InvalidConsumptionValueError
    
    new_goal = Goal(
        starting_date=new_starting_date,
        ending_date=new_ending_date,
        si_measurement_unit=new_si_measurement_unit.lower(),
        value=new_value,
        creator_id=current_user.id,
        creator=current_user.username
        )
    
    with get_session() as session:
        session.add(new_goal)
        session.flush()
        
    return new_goal
    
    
def get_user_goals(current_user : User, 
                                 target_measurement_unit: Optional[str] = None, 
                                 target_starting_date: Optional[date] = None,
                                 target_ending_date: Optional[date] = None,
                                 minimum_value: Optional[Decimal] = None, 
                                 maximum_value: Optional[Decimal] = None
                                 ):
    if current_user == None:
        raise UserNotFoundError
    
    if (maximum_value != None) and (minimum_value != None):
        if minimum_value > maximum_value:
            raise InvalidConsumptionValueError
    
    if (target_ending_date != None) and (target_starting_date != None):
        if target_starting_date > target_ending_date:
            raise InvalidDateError

    stmt = select(Goal).where(Goal.creator_id == current_user.id)
    
    if target_measurement_unit != None:
        stmt = stmt.where(Goal.si_measurement_unit == target_measurement_unit.lower())
    
    # comparação por igualdade ou maioridade, pois quero datas depois da data de início
    if target_starting_date != None:
        stmt = stmt.where(Goal.starting_date >= target_starting_date)
        
    if target_ending_date != None:
        stmt = stmt.where(Goal.ending_date <= target_ending_date)
        
    if minimum_value != None:
        stmt = stmt.where(Goal.value >= minimum_value)
        
    if maximum_value != None:
        stmt = stmt.where(Goal.value <= maximum_value)
    
    # All já trata os scalars como objetos separados, pois ele os consome inteiros
    with get_session() as session:
        goals = session.scalars(stmt).all()
        
        if goals == []:
            raise ConsumptionsNotFoundError
        
    return goals


def edit_goal(current_user: User,
                     target_goal_id: int,
                     new_starting_date: Optional[date] = None,
                     new_ending_date: Optional[date] = None,
                     new_measurement_unit: Optional[str] = None,
                     new_value: Optional[Decimal] = None):
    if current_user == None:
        raise UserNotFoundError
    
    if (new_value != None) and (new_value <= 0):
        raise InvalidConsumptionValueError
    
    with get_session() as session:
        to_edit = get_owned_goals(session, current_user, target_goal_id)

        if (new_starting_date != None) and (new_starting_date > to_edit.ending_date):
            raise InvalidDateError

        if (new_ending_date != None) and (new_ending_date < to_edit.starting_date):
            raise InvalidDateError
    
        if new_starting_date != None:
            to_edit.starting_date = new_starting_date
            
        if new_ending_date != None:
            to_edit.ending_date = new_ending_date
            
        if new_measurement_unit != None:
            to_edit.si_measurement_unit = new_measurement_unit.lower()
            
        if new_value != None:
            to_edit.value = new_value
            
    return to_edit


def delete_goal(current_user: User, target_goal_id: int):
    if current_user == None:
        raise UserNotFoundError
    
    if current_user == None:
        raise UserNotFoundError
    
    to_delete = get_owned_goals(session, current_user, target_goal_id)
    with get_session() as session:
        session.delete(to_delete)
        
