from fastapi import APIRouter, Depends, HTTPException  # importar do fast api o roteador
from src.models.user_model import User
from src.database.session import get_session
from src.schemas.user_schemas import UserSchema, UpdateUserSchema, Token, ForgotPasswordSchema
from jwt import PyJWKClient
from src.api.security import OAuth2PasswordRequestForm, create_acess_token
from http import HTTPStatus
from src.controllers.user_controller import login, create_user, edit_user_password, edit_user_real_name, edit_user_username, edit_user_email, delete_self, get_user_by_email
from src.errors.user_errors import EmailAlreadyExistsError, AppError, UsernameAlreadyExistsError, UserNotFoundError, InvalidUsernameError, InvalidCredentialsError, InvalidEmailError
from src.api.security import get_current_user, create_access_token
from src.api.email_config import conf
from fastapi_mail import FastMail, MessageSchema

user_router = APIRouter(prefix= "/users", tags= ["usuarios"])

@user_router.post("/criar_usuario")
async def register_user(user_schema: UserSchema):
 try:
    create_user(user_schema.username, user_schema.email, user_schema.password, user_schema.real_name)
 except EmailAlreadyExistsError as e:
    raise HTTPException(status_code=e.status_code, detail=e.message)
 
 except UsernameAlreadyExistsError as e:
    raise HTTPException(status_code=e.status_code, detail=e.message) 
 
 except InvalidEmailError as e:
    raise HTTPException(status_code=e.status_code, detail=e.message)
 
 except InvalidUsernameError as e:
    raise HTTPException(status_code=e.status_code, detail=e.message)
 
 return {"mensagem" : "usuário cadastrado com sucesso  "}
    

@user_router.put("/editar_usuario")
async def update_user(user_schema: UpdateUserSchema, current_user: User = Depends(get_current_user)):
  if user_schema.new_name is not None:
   try:
     edit_user_username(current_user, user_schema.new_name)
   except UsernameAlreadyExistsError as e:
    raise HTTPException(status_code=e.status_code, detail=e.message) 
   
  if user_schema.new_password is not None:
    try:
     edit_user_password(current_user, user_schema.new_password)
    except InvalidCredentialsError as e:
     raise HTTPException(status_code=e.status_code, detail=e.message) 
    
  if user_schema.new_email is not None:
    try:
     edit_user_email(current_user, user_schema.new_email)
    except InvalidEmailError as e:
     raise HTTPException(status_code=e.status_code, detail=e.message)

  if user_schema.real_name is not None:
   try:
     edit_user_real_name(current_user, user_schema.real_name)
   except UsernameAlreadyExistsError as e:
     raise HTTPException(status_code=e.status_code, detail=e.message)

   return{"mensagem" : "usuário editado com sucesso  "}
     

@user_router.delete("/excluir_usuario")
async def delete_user(current_user: User = Depends(get_current_user)):
  try:
   delete_self(current_user)
  except UserNotFoundError as e:
    raise HTTPException(status_code=e.status_code, detail=e.message)
  return{"mensagem" : "usuário excluído com sucesso !"}
  
    
@user_router.post("/login_usuario_token", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm):
 try:
   user = login(form_data.username, form_data.password)
   access_token = create_acess_token(data={'sub' : user.email})

 except UserNotFoundError as e:
   raise HTTPException(status_code=e.status_code, detail=e.message)
 
 except InvalidCredentialsError as e:
   raise HTTPException(status_code=e.status_code, detail=e.message)
 
 return user
 
@user_router.post("/esqueci_a_senha")
async def forgotten_password(user_schema: ForgotPasswordSchema):
    try:
        user = get_user_by_email(user_schema.email)
        token = create_access_token(data={'sub': user_schema.email})
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





