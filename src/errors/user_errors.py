from src.errors.app_errors import AppError
from fastapi import status

class InvalidUsernameError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    status_name = 'INVALID_USERNAME'
    message = 'O Username que você tentou cadastrar é inválido. Utilize apenas letras, números, . e _.'
    


class InvalidEmailError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    status_name = 'INVALID_EMAIL'
    message = 'O Email que você cadastrar inserir é inválido ou inexistente. Por favor, tente novamente.'



class InvalidPasswordError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    status_name = 'INVALID_PASSWORD'
    message = 'A senha que você tentou cadastrar não cumpre com os parâmetros. Por favor, tente novamente.'
    
    
    
class InvalidCredentialsError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    status_name = 'INVALID_CREDENTIALS'
    message = 'As credenciais do usuário estão incorretas. Por favor, tente novamente.'



class UserNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    status_name = 'USER_NOT_FOUND'
    message = 'O usuário requisitado não foi encontrado. Por favor, tente novamente.'



class UsernameAlreadyExistsError(AppError):
    status_code = status.HTTP_409_CONFLICT
    status_name = 'USERNAME_ALREADY_EXISTS'
    message = 'O Username que você tentou inserir já existe no sistema. Faça login ou tente novamente.'
    
    

class EmailAlreadyExistsError(AppError):
    status_code = status.HTTP_409_CONFLICT
    status_name = 'EMAIL_ALREADY_EXISTS'
    message = 'O Email que você tentou inserir já existe no sistema. Faça login ou tente novamente.'



