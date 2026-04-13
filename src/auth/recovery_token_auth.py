from fastapi import HTTPException, status
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

def create_recovery_token(user_to_recover: User):
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=(int(os.getenv('RECOVERY_TOKEN_EXPIRE_MINUTES'))))
    
    header = {"alg": os.getenv('ALGORITHM'),
              "typ": "JWT",}
    
    payload = {'exp': expire,
               'sub': user_to_recover.id,
               'type': 'recovery'}
    
    encoded_jwt = jwt.encode(headers=header,
                             payload=payload,
                             algorithm=os.getenv('ALGORITHM'),
                             key=os.getenv('RECOVERY_TOKEN_KEY'))

    return encoded_jwt


def get_user_to_recover(token):
    try:    
        to_decode = jwt.decode(jwt=token,
                               key=os.getenv('RECOVERY_TOKEN_KEY'),
                               algorithms=[os.getenv('ALGORITHM')])
        
        if to_decode.get('type') != 'recovery':
            raise WrongTokenTypeError

        user_id = to_decode.get('sub')
        current_user = get_user_by_id(user_id)

        return current_user

    except WrongTokenTypeError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='O tempo para recuperação expirou. Por favor, tente novamente.')
    
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Houve uma falha ao tentar recuperar a senha. Por favor, tente novamente.')
