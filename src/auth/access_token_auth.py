import os
from datetime import datetime, timezone, timedelta
from uuid import uuid4

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from dotenv import load_dotenv

from src.models.user_model import User
from src.controllers.user_controller import get_user_by_id
from src.clients.redis_client import redis_client
from src.errors.user_errors import *

load_dotenv()

# OAuth2: define como um cliente acessa os recursos do sistema
# Cria tokens que realizam as ações no sistema
# Essa função pegará o token do header HTTP 'Authorization'
# Especificamente o token gerado pela create_access_token e armazenado no frontend
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login_usuario", refreshUrl="/usuarios/regerar_token")

def create_access_token(current_user: User):
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=(int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))))
    jti = str(uuid4())
    
    header = {"alg": os.getenv('ALGORITHM'),
              "typ": "JWT",}
    
    payload = {'exp': expire,
               'sub': str(current_user.id),
               'jti': jti,
               'type': 'access'}
    
    encoded_jwt = jwt.encode(headers=header,
                             payload=payload,
                             algorithm=os.getenv('ALGORITHM'),
                             key=os.getenv('ACCESS_TOKEN_KEY'))

    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        decoded_token = jwt.decode(jwt=token,
                               key=os.getenv('ACCESS_TOKEN_KEY'),
                               algorithms=[os.getenv('ALGORITHM')])
        
        if decoded_token.get('type') != 'access':
            raise InvalidTokenTypeError
        
        jti = decoded_token.get('jti')
        if redis_client.exists(f'blacklisted:{jti}') == True:
            raise BlacklistedTokenError

        user_id = int(decoded_token.get('sub'))
        current_user = get_user_by_id(user_id)

        return current_user

    except InvalidTokenTypeError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except BlacklistedTokenError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='O seu tempo de login expirou. Por favor autentique-se novamente.')
    
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Houve uma falha ao autenticar seu usuário. Por favor, tente novamente.')


# Lembrete: o campo 'sub' do JWT tem que ser uma string, então devemos mudar isso em todo o sistema e converter quando necessário.