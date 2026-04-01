from jwt import encode, decode
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException 
from datetime import datetime,timedelta
from dotenv import load_dotenv
from zoneinfo import ZoneInfo
import os
from database import session
from src.database.engine import get_session
from src.models.user_model import User

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login_usuario_token")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))
    return encoded_jwt

def get_current_user(token:str= Depends(oauth2_scheme)):
 try:   
    to_decode = decode(token, os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
    email = to_decode.get('sub')

 except:
    raise HTTPException(status_code=401)
 
 if email is not None:
    raise HTTPException(status_code=401)
 
 with get_session() as session:
     user = session.query(User).filter(User.email == email).first()
 return user
