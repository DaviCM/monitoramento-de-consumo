from app_error import AppError
from fastapi import status

class InvalidCredentialsError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    status_name = 'UNAUTHORIZED'
    message = 'As credenciais do usuário estão incorretas.'
