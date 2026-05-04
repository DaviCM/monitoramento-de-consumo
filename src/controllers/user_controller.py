from typing import Optional

from sqlalchemy import select
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import SecretStr

from src.models.user_model import User
from src.schemas.user_schemas import UserSchema, UpdateUserSchema
from src.database.session import get_session
from src.errors.user_errors import *
from src.validators import email_validators, password_validators, username_validators


argon2 = PasswordHasher()

def verify_password(hashed_password, password):
    try:
        return argon2.verify(hashed_password, password)
    except VerifyMismatchError:
        return False


def create_user(params: UserSchema):
    if email_validators.verify_email(params.email) == False:
        raise InvalidEmailError
    
    if email_validators.email_already_exists(params.email) == True:
        raise EmailAlreadyExistsError
    
    if username_validators.verify_username(params.username) == False:
        raise InvalidUsernameError
    
    if username_validators.username_already_exists(params.username) == True:
        raise UsernameAlreadyExistsError
    
    if password_validators.verify_password(params.password.get_secret_value()) == False:
        raise InvalidPasswordError
    
    new_user = User(**(params.model_dump()))

    with get_session() as session:
        session.add(new_user)
        session.flush()
        
    return new_user
        

def login(user_email: str, user_password: SecretStr):
    stmt = select(User).where(User.email == user_email)
    with get_session() as session:
        returned_user = session.scalar(stmt)
        
    if returned_user == None:
        raise UserNotFoundError
    
    hashed_password = returned_user.password
    
    if verify_password(hashed_password, user_password.get_secret_value()) == False:
        raise InvalidCredentialsError
    else:
        return returned_user


def edit_user(current_user: User, params: UpdateUserSchema):
    
    if current_user == None:
        raise UserNotFoundError
    
    if (params.new_username != None) and (username_validators.verify_username(params.new_username) == False):
        raise InvalidUsernameError
    
    if (params.new_username != None) and (username_validators.username_already_exists(params.new_username) == True):
        raise UsernameAlreadyExistsError

    if (params.new_email != None) and (email_validators.verify_email(params.new_email) == False):
        raise InvalidEmailError
    
    if (params.new_email != None) and (email_validators.email_already_exists(params.new_email) == True):
        raise EmailAlreadyExistsError
    
    if (params.new_password != None) and (password_validators.verify_password(params.new_password.get_secret_value()) == False):
        raise InvalidPasswordError
    
    
    with get_session() as session:
        # session.merge reintegra um objeto detached à sessão corrente, ideal para sabermos quem é o usuário antes de o manipular.
        to_edit = session.merge(current_user)
        
        if params.new_real_name != None:
            to_edit.real_name = params.new_real_name
        
        if params.new_username != None:
            to_edit.username = params.new_username
            
        if params.new_email != None:
            to_edit.email = params.new_email.lower()
        
        if params.new_password != None:
            to_edit.password = argon2.hash(params.new_password.get_secret_value())

    return to_edit


def delete_self(current_user: User):
    if current_user == None:
        raise UserNotFoundError
    
    with get_session() as session:
        to_delete = session.merge(current_user)
        session.delete(to_delete)


def get_user_by_id(target_id):
    stmt = select(User).where(User.id == target_id)
    with get_session() as session:
        user = session.scalar(stmt)
        
    if user == None:
        raise UserNotFoundError
        
    return user
  

def get_user_by_email(email: str):
    stmt = select(User).where(User.email == email.lower())
    with get_session() as session:
        user = session.scalar(stmt)
        
    if user is None:
        raise UserNotFoundError
    
    return user
    
    