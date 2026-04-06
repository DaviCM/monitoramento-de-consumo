from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from datetime import timedelta
from src.models.user_model import User
from src.controllers.user_controller import get_user_by_id
from src.errors.user_errors import *
import jwt
import os

load_dotenv()

# OAuth2: define como um cliente acessa os recursos do sistema
# Cria tokens que realizam as ações no sistema
# Essa função pegará o token do header HTTP 'Authorization'
# Especificamente o token gerado pela create_access_token e armazenado no frontend
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def create_access_token(current_user: User):
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=(int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))))
    
    header = {"alg": os.getenv('ALGORITHM'),
              "typ": "JWT",}
    
    payload = {'exp': expire,
               'sub': current_user.id,}
    
    encoded_jwt = jwt.encode(headers=header,
                             payload=payload,
                             algorithm=os.getenv('ALGORITHM'),
                             key=os.getenv('ACCESS_TOKEN_KEY'))

    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    to_decode = jwt.decode(jwt=token,
                           key=os.getenv('ACCESS_TOKEN_KEY'),
                           algorithms=[os.getenv('ALGORITHM')])
    
    user_id = to_decode.get('sub')
    current_user = get_user_by_id(user_id)
    
    return current_user


def create_recovery_token(user_to_recover: User):
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=(int(os.getenv('RECOVERY_TOKEN_EXPIRE_MINUTES'))))
    
    header = {"alg": os.getenv('ALGORITHM'),
              "typ": "JWT",}
    
    payload = {'exp': expire,
               'sub': user_to_recover.id,}
    
    encoded_jwt = jwt.encode(headers=header,
                             payload=payload,
                             algorithm=os.getenv('ALGORITHM'),
                             key=os.getenv('RECOVERY_TOKEN_KEY'))

    return encoded_jwt


def get_user_to_recover(token):
    to_decode = jwt.decode(jwt=token,
                           key=os.getenv('RECOVERY_TOKEN_KEY'),
                           algorithms=[os.getenv('ALGORITHM')])
    
    user_id = to_decode.get('sub')
    current_user = get_user_by_id(user_id)
    
    return current_user