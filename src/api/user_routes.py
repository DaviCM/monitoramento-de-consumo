from fastapi import APIRouter, Depends, HTTPException  # importar do fast api o roteador
from src.models.user_model import User
from src.database.session import get_session
from src.schemas.user_schemas import UserSchema, UpdateUserSchema, Token
from jwt import PyJWKClient
from src.api.security import OAuth2PasswordRequestForm, create_acess_token
from http import HTTPStatus
from src.controllers.user_controller import login, create_user, edit_user_password, edit_user_real_name, edit_user_username, edit_user_email, delete_self
from src.errors.user_errors import EmailAlreadyExistsError, AppError, UsernameAlreadyExistsError, UserNotFoundError, InvalidUsernameError, InvalidCredentialsError, InvalidEmailError
from src.api.security import get_current_user

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
async def update_user(user_schema: UpdateUserSchema):
  if user_schema.new_name is not None:
   try:
     edit_user_username(user_schema.new_name)
   except UsernameAlreadyExistsError as e:
    raise HTTPException(status_code=e.status_code, detail=e.message) 
   
  elif user_schema.new_password is not None:
    try:
     edit_user_password(user_schema.new_password)
    except InvalidCredentialsError as e:
     raise HTTPException(status_code=e.status_code, detail=e.message) 
    
  elif user_schema.new_email is not None:
    try:
     edit_user_email(user_schema.new_email)
    except InvalidCredentialsError as e:
     raise HTTPException(status_code=e.status_code, detail=e.message)

  elif user_schema.real_name is not None:
   try:
     edit_user_real_name(user_schema.real_name)
   except UsernameAlreadyExistsError as e:
     raise HTTPException(status_code=e.status_code, detail=e.message)

   return{"mensagem" : "usuário editado com sucesso  "}
    

@user_router.delete("/excluir_usuario")
async def delete_user(user_schema: get_current_user):
  try:
    delete_self(user_schema,get_current_user)
  except UserNotFoundError as e:
    raise HTTPException(status_code=e.status_code, detail=e.message)
  return{"mensagem" : "usuário excluído com sucesso !"}
  
    
@user_router.post("/login_usuario_token", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm):
  try:
    access_token = login(form_data.username, form_data.password)

  except UserNotFoundError as e:
    raise HTTPException(status_code=e.status_code, detail=e.message)
 
  except InvalidCredentialsError as e:
    raise HTTPException(status_code=e.status_code, detail=e.message)
 
  return {'acess_token': access_token, 'token_type' : 'bearer'}
 

@user_router.post("esqueci_a_senha")
async def forgotten_password(user_schema: UserSchema):
 pass



   


