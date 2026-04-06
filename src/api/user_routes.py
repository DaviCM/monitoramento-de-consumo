from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_mail import FastMail, MessageSchema
from jwt import ExpiredSignatureError, InvalidTokenError
from src.models.user_model import User
from src.schemas.user_schemas import *
from src.schemas.token_schemas import *
from src.controllers.user_controller import *
from src.errors.user_errors import *
from src.api.security import *
from src.api.email_config import conf

user_router = APIRouter(prefix="/users", tags=["Usuário"])

@user_router.post(path="/criar_usuario", status_code=status.HTTP_201_CREATED, response_model=ResponseUserSchema)
async def create_user_route(new_user: UserSchema):
    try:
        return create_user(new_user.real_name, 
                           new_user.username, 
                           new_user.email, 
                           new_user.password)
        
    except EmailAlreadyExistsError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except UsernameAlreadyExistsError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except InvalidEmailError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except InvalidUsernameError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)



@user_router.patch(path="/editar_usuario", status_code=status.HTTP_200_OK, response_model=ResponseUserSchema)
async def edit_user_route(params: UpdateUserSchema, current_user: User = Depends(get_current_user)):
    try:
        return edit_user(current_user=current_user,
                         new_real_name=params.new_real_name,
                         new_username=params.new_username,
                         new_email=params.new_email,
                         new_password=params.new_password)
            
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except InvalidUsernameError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except UsernameAlreadyExistsError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except InvalidEmailError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except EmailAlreadyExistsError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)



@user_router.delete(path="/deletar_usuario", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_route(current_user: User = Depends(get_current_user)):
    try:
        delete_self(current_user)
        
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)



@user_router.post(path="/login_usuario_token", status_code=status.HTTP_302_FOUND, response_model=Token)
async def login_route(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = login(form_data.username, form_data.password)
        token = create_access_token(user)
        return {'access_token': token, 'token_type': 'bearer'}
    
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)



@user_router.post(path="/esqueci_a_senha", status_code=status.HTTP_204_NO_CONTENT)
async def forgotten_password(user_email):
    try:
        user = get_user_by_email(user_email)
        token = create_recovery_token(user)
        
        message = MessageSchema(
            subject="Redefinição de senha",
            recipients=[user_email],
            # Esse token estará no link, por isso ele pode ser passado como parâmetro direto na função abaixo
            body=f"Aqui o token para redefinição de senha: {token}",
            subtype="plain"
        )
        
        fm = FastMail(conf)
        await fm.send_message(message)
        
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    

@user_router.post(path='/recuperacao_de_senha', status_code=status.HTTP_200_OK, response_model=ResponseUserSchema)
async def password_recovery(new_password: str, token: str):
    try:
        current_user = get_user_to_recover(token)
        
        return edit_user(current_user=current_user,
                         new_password=new_password)
    
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='O tempo para recuperação expirou. Por favor, tente novamente.')
    
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Houve uma falha ao tentar recuperar a senha. Por favor, tente novamente.')
    
    
    
    
