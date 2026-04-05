from jwt import encode
import jwt
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

def create_access_token(user_id: int):
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    
    header = {"alg": os.getenv('ALGORITHM'), "typ": "JWT"}
    
    payload = {'exp': expire, 'sub': str(user_id)}
    
    encoded_jwt = jwt.encode(headers=header,
                             payload=payload,
                             algorithm=os.getenv('ALGORITHM'),
                             key=os.getenv('SECRET_TOKEN_KEY'))
    return encoded_jwt