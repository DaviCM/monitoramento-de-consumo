from src.models.user_model import User
from src.database.session import get_session
from src.errors.user_errors import *
from src.validators import email_validators, password_validators, username_validators
from sqlalchemy import select
from argon2 import PasswordHasher
from typing import Optional


argon2 = PasswordHasher()

def verify_password(hashed_password, password):
    return argon2.verify(hashed_password, password)


def create_user(new_real_name, new_username, new_email, new_password):
    if email_validators.verify_email(new_email) == False:
        raise InvalidEmailError
    
    if email_validators.email_already_exists(new_email) == True:
        raise EmailAlreadyExistsError
    
    if username_validators.verify_username(new_username) == False:
        raise InvalidUsernameError
    
    if username_validators.username_already_exists(new_username) == True:
        raise UsernameAlreadyExistsError
    
    if password_validators.verify_password(new_password) == False:
        raise InvalidPasswordError
    
    new_user = User(
        real_name=new_real_name,
        username=new_username,
        email=new_email,
        password=argon2.hash(new_password)
        )

    with get_session() as session:
        session.add(new_user)
        session.flush()
        
    return new_user
        

def login(user_email, user_password):
    stmt = select(User).where(User.email == user_email)
    with get_session() as session:
        returned_user = session.scalar(stmt)
        
    if returned_user == None:
        raise UserNotFoundError
    
    hashed_password = returned_user.password
    
    if verify_password(hashed_password, user_password) == False:
        raise InvalidCredentialsError
    else:
        return returned_user


def edit_user(current_user: User,
              new_real_name: Optional[str] = None,
              new_username: Optional[str] = None,
              new_email: Optional[str] = None,
              new_password: Optional[str] = None,
              ):
    
    if current_user == None:
        raise UserNotFoundError
    
    if (new_username != None) and (username_validators.verify_username(new_username) == False):
        raise InvalidUsernameError
    
    if (new_username != None) and (username_validators.username_already_exists(new_username) == True):
        raise UsernameAlreadyExistsError

    if (new_email != None) and (email_validators.verify_email(new_email) == False):
        raise InvalidEmailError
    
    if (new_email != None) and (email_validators.email_already_exists(new_email) == True):
        raise EmailAlreadyExistsError
    
    if (new_password != None) and (password_validators.verify_password(new_password) == False):
        raise InvalidPasswordError
    
    
    with get_session():
        if new_real_name != None:
            current_user.real_name = new_real_name
        
        if new_username != None:
            current_user.username = new_username
            
        if new_email != None:
            current_user.email = new_email
        
        if new_password != None:
            current_user.password = argon2.hash(new_password)

    return current_user


def delete_self(current_user: User):
    if current_user == None:
        raise UserNotFoundError
    
    with get_session() as session:
            session.delete(current_user)


def get_user_by_id(target_id):
    stmt = select(User).where(User.id == target_id)
    with get_session() as session:
        user = session.scalar(stmt)
        
    if user == None:
        raise UserNotFoundError
        
    return user
  

def get_user_by_email(email: str):
    stmt = select(User).where(User.email == email)
    with get_session() as session:
        user = session.scalar(stmt)
        
    if user is None:
        raise UserNotFoundError
    
    return user
    
    