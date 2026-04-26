import os
from datetime import datetime, timezone, timedelta
from typing import Literal # Literal: apenas valores nesse grupo restrito de valores será aceito!

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException, status
from src.clients.redis_client import redis_client

def blacklist_token(token: str, token_type: Literal['access', 'refresh']):
    if token_type == 'access':
        token_key = 'ACCESS_TOKEN_KEY'

    elif token_type == 'refresh':
        token_key = 'REFRESH_TOKEN_KEY'

    try:
        decoded_token = jwt.decode(jwt=token,
                                   key=os.getenv(token_key),
                                   algorithms=[os.getenv('ALGORITHM')])

        jti = decoded_token.get('jti')
        token_expire = datetime.fromtimestamp(decoded_token.get('exp'))
        redis_client.set(name=f'blacklisted:{jti}', 
                         value=1,
                         ex=(token_expire - datetime.now(tz=timezone.utc)))
    
    except ExpiredSignatureError:
        pass

    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Houve uma falha ao realizar seu logout. Tente novamente mais tarde.')


def invalidate_recovery_token(token):
    try:
        decoded_token = jwt.decode(jwt=token,
                                   key=os.getenv('RECOVERY_TOKEN_KEY'),
                                   algorithms=[os.getenv('ALGORITHM')])
        
        jti = decoded_token.get('jti')
        token_expire = datetime.fromtimestamp(decoded_token.get('exp'))
        redis_client.set(name=f'used:{jti}',
                         value=1,
                         ex=token_expire - datetime.now(tz=timezone.utc))

    except ExpiredSignatureError:
        pass

    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Houve uma falha ao recuperar sua senha. Por favor, tente novamente.')

    