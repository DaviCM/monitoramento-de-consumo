from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from dotenv import load_dotenv
from src.controllers.user_controller import get_user_by_id
from src.errors.user_errors import UserNotFoundError
import jwt
import os


load_dotenv()

# OAuth2: define como um cliente acessa os recursos do sistema
# Cria tokens que realizam as ações no sistema
# Essa função pegará o token do header HTTP 'Authorization'
# Especificamente o token gerado pela create_access_token e armazenado no frontend
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login_usuario_token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        to_decode = jwt.decode(jwt=token,
                               key=os.getenv('SECRET_TOKEN_KEY'),
                               algorithms=[os.getenv('ALGORITHM')])
        user_id = int(to_decode.get('sub'))
        current_user = get_user_by_id(user_id)
        return current_user
    except UserNotFoundError:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")


