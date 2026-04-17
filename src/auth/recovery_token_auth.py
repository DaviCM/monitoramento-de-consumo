import os
from datetime import datetime, timezone, timedelta
from uuid import uuid4

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException, status
from dotenv import load_dotenv

from src.models.user_model import User
from src.controllers.user_controller import get_user_by_id
from src.redis.redis_client import redis_client
from src.errors.user_errors import *

load_dotenv()

def create_recovery_token(user_to_recover: User):
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=(int(os.getenv('RECOVERY_TOKEN_EXPIRE_MINUTES'))))
    jti = str(uuid4())
    
    header = {"alg": os.getenv('ALGORITHM'),
              "typ": "JWT",}
    
    payload = {'exp': expire,
               'sub': str(user_to_recover.id),
               'jti': jti,
               'type': 'recovery'}
    
    encoded_jwt = jwt.encode(headers=header,
                             payload=payload,
                             algorithm=os.getenv('ALGORITHM'),
                             key=os.getenv('RECOVERY_TOKEN_KEY'))

    return encoded_jwt


def get_user_to_recover(token):
    try:    
        decoded_token = jwt.decode(jwt=token,
                               key=os.getenv('RECOVERY_TOKEN_KEY'),
                               algorithms=[os.getenv('ALGORITHM')])
        
        if decoded_token.get('type') != 'recovery':
            raise InvalidTokenTypeError

        user_id = int(decoded_token.get('sub'))
        current_user = get_user_by_id(user_id)

        return current_user

    except InvalidTokenTypeError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='O tempo para recuperação expirou. Por favor, tente novamente.')
    
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Houve uma falha ao tentar recuperar a senha. Por favor, tente novamente.')
