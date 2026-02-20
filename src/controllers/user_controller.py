from models.user_model import User
from database.session import get_session
from errors.user_errors import *
from validators import email_validators, password_validators, username_validators
from sqlalchemy import select
from argon2 import PasswordHasher

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
    
    new_user = User(
        real_name=new_real_name,
        username=new_username,
        email=new_email,
        password=argon2.hash(new_password)
        )

    with get_session() as session:
        session.add(new_user)
        

def login(user_email, user_password):
    stmt = select(User).where(User.email == user_email)
    with get_session() as session:
        returned_user = session.scalar(stmt)
        
    if returned_user == None:
        raise InvalidCredentialsError
    
    hashed_password = returned_user.password
    
    if verify_password(hashed_password, user_password) == False:
        raise InvalidCredentialsError
    else:
        return returned_user


def edit_user_real_name(current_user: User, new_real_name):
    with get_session():
        current_user.real_name = new_real_name
    
    
def edit_user_username(current_user: User, new_username):
    if username_validators.username_already_exists(new_username) == True:
        raise UsernameAlreadyExistsError
    
    with get_session():
        current_user.username = new_username
        

def edit_user_password(current_user: User, new_password):
    pass