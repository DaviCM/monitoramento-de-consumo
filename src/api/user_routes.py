from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.models.user_model import User
from src.schemas.user_schemas import UserSchema, UpdateUserSchema, Token, ForgotPasswordSchema
from src.controllers.user_controller import login, create_user, edit_user_password, edit_user_real_name, edit_user_username, edit_user_email, delete_self, get_user_by_email
from src.errors.user_errors import EmailAlreadyExistsError, UsernameAlreadyExistsError, UserNotFoundError, InvalidUsernameError, InvalidCredentialsError, InvalidEmailError
from src.api.security import get_current_user
from src.api.email_config import conf
from fastapi_mail import FastMail, MessageSchema
from src.token import create_access_token

user_router = APIRouter(prefix="/users", tags=["usuarios"])

@user_router.post("/criar_usuario")
async def register_user(user_schema: UserSchema):
    try:
        create_user(user_schema.real_name, user_schema.username, user_schema.email, user_schema.password)
    except EmailAlreadyExistsError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except UsernameAlreadyExistsError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except InvalidEmailError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except InvalidUsernameError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return {"mensagem": "usuário cadastrado com sucesso"}


@user_router.put("/editar_usuario")
async def update_user(user_schema: UpdateUserSchema, current_user: User = Depends(get_current_user)):
    try:
        if user_schema.new_name is not None:
            edit_user_username(current_user, user_schema.new_name)
        if user_schema.new_password is not None:
            edit_user_password(current_user, user_schema.new_password)
        if user_schema.new_email is not None:
            edit_user_email(current_user, user_schema.new_email)
        if user_schema.real_name is not None:
            edit_user_real_name(current_user, user_schema.real_name)
    except UsernameAlreadyExistsError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except InvalidEmailError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return {"mensagem": "usuário editado com sucesso"}


@user_router.delete("/excluir_usuario")
async def delete_user(current_user: User = Depends(get_current_user)):
    try:
        delete_self(current_user)
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return {"mensagem": "usuário excluído com sucesso!"}


@user_router.post("/login_usuario_token", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        token = login(form_data.username, form_data.password)
        return {'access_token': token, 'token_type': 'bearer'}
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@user_router.post("/esqueci_a_senha")
async def forgotten_password(user_schema: ForgotPasswordSchema):
    try:
        user = get_user_by_email(user_schema.email)
        token = create_access_token(user.id)
        message = MessageSchema(
            subject="Redefinição de senha",
            recipients=[user_schema.email],
            body=f"Aqui o token para redefinição de senha: {token}",
            subtype="plain"
        )
        fm = FastMail(conf)
        await fm.send_message(message)
        edit_user_password(user, user_schema.new_password)
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return {"mensagem": "Email de redefinição de senha enviado."}