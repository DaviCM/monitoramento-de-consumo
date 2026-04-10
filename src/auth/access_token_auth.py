from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from datetime import timedelta
from src.models.user_model import User
from src.controllers.user_controller import get_user_by_id
from src.errors.user_errors import *
from jwt import ExpiredSignatureError, InvalidTokenError
import jwt

import os

load_dotenv()

# OAuth2: define como um cliente acessa os recursos do sistema
# Cria tokens que realizam as ações no sistema
# Essa função pegará o token do header HTTP 'Authorization'
# Especificamente o token gerado pela create_access_token e armazenado no frontend
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login_usuario_token")

def create_access_token(current_user: User):
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=(int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))))
    
    header = {"alg": os.getenv('ALGORITHM'),
              "typ": "JWT",}
    
    payload = {'exp': expire,
               'sub': current_user.id,
               'type': 'access'}
    
    encoded_jwt = jwt.encode(headers=header,
                             payload=payload,
                             algorithm=os.getenv('ALGORITHM'),
                             key=os.getenv('ACCESS_TOKEN_KEY'))

    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        to_decode = jwt.decode(jwt=token,
                               key=os.getenv('ACCESS_TOKEN_KEY'),
                               algorithms=[os.getenv('ALGORITHM')])
        
        if to_decode.get('type') != 'access':
            raise WrongTokenTypeError

        user_id = to_decode.get('sub')
        current_user = get_user_by_id(user_id)

        return current_user

    except WrongTokenTypeError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='O seu tempo de login expirou. Por favor autentique-se novamente.')
    
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Houve uma falha ao autenticar seu usuário. Por favor, tente novamente.')

