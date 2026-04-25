import os
from datetime import datetime, timezone, timedelta
from uuid import uuid4

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException, status
from dotenv import load_dotenv

from src.auth.access_token_auth import create_access_token
from src.models.user_model import User
from src.controllers.user_controller import get_user_by_id
from src.clients.redis_client import redis_client
from src.errors.user_errors import *


load_dotenv()

def create_refresh_token(current_user: User):
    expire = datetime.now(tz=timezone.utc) + timedelta(days=(int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS'))))
    jti = str(uuid4())
    
    header = {"alg": os.getenv('ALGORITHM'),
              "typ": "JWT",}
    
    payload = {'exp': expire,
               'sub': str(current_user.id),
               'jti': jti,
               'type': 'refresh'}
    
    encoded_jwt = jwt.encode(headers=header,
                             payload=payload,
                             algorithm=os.getenv('ALGORITHM'),
                             key=os.getenv('REFRESH_TOKEN_KEY'))

    return encoded_jwt


def refresh_current_user(token: str):
    try:
        decoded_token = jwt.decode(jwt=token,
                               key=os.getenv('REFRESH_TOKEN_KEY'),
                               algorithms=[os.getenv('ALGORITHM')])
        
        if decoded_token.get('type') != 'refresh':
            raise InvalidTokenTypeError
        
        jti = decoded_token.get('jti')
        if redis_client.exists(f'blacklisted:{jti}') == True:
            raise BlacklistedTokenError

        user_id = int(decoded_token.get('sub'))
        current_user = get_user_by_id(user_id)

        return create_access_token(current_user)

    except InvalidTokenTypeError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except BlacklistedTokenError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='O seu tempo de login expirou. Por favor autentique-se novamente.')
    
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Houve uma falha ao autenticar seu usuário. Por favor, tente novamente.')
    
    