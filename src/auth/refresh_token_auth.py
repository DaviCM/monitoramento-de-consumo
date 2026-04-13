from fastapi import HTTPException, status
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from datetime import timedelta
from src.auth.access_token_auth import create_access_token
from src.models.user_model import User
from src.controllers.user_controller import get_user_by_id
from src.errors.user_errors import *
from jwt import ExpiredSignatureError, InvalidTokenError
import jwt

import os

load_dotenv()

def create_refresh_token(current_user: User):
    expire = datetime.now(tz=timezone.utc) + timedelta(days=(int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS'))))
    
    header = {"alg": os.getenv('ALGORITHM'),
              "typ": "JWT",}
    
    payload = {'exp': expire,
               'sub': current_user.id,
               'type': 'refresh',}
    
    encoded_jwt = jwt.encode(headers=header,
                             payload=payload,
                             algorithm=os.getenv('ALGORITHM'),
                             key=os.getenv('REFRESH_TOKEN_KEY'))

    return encoded_jwt


def refresh_current_user(token: str):
    try:
        to_decode = jwt.decode(jwt=token,
                               key=os.getenv('REFRESH_TOKEN_KEY'),
                               algorithms=[os.getenv('ALGORITHM')])
        
        if to_decode.get('type') != 'refresh':
            raise WrongTokenTypeError

        user_id = to_decode.get('sub')
        current_user = get_user_by_id(user_id)

        return create_access_token(current_user)

    except WrongTokenTypeError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='O seu tempo de login expirou. Por favor autentique-se novamente.')
    
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Houve uma falha ao autenticar seu usuário. Por favor, tente novamente.')
    
    