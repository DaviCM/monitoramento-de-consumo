from fastapi import APIRouter, Depends, HTTPException # importar do fast api o roteador
from src.models.user_model import User
from src.api.dependencies import pegar_sessao
from src.schemas.user_schemas import UserSchema, UserUpdateSchema
from jwt import PyJWKClient

user_router = APIRouter(prefix= "/users", tags= ["usuarios"])

@user_router.post("/criar_usuario")
async def create_user(user_schema: UserSchema, session = Depends(pegar_sessao)):
    user = session.query(User).filter(User.email==user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email do usuário já foi cadastrado")
    else:
       new_user = User(
    username=user_schema.username,
    email=user_schema.email,
    password=user_schema.password,
    real_name=user_schema.real_name
)
    session.add(new_user)
    session.commit()
    return {"mensagem" : "usuário cadastrado com sucesso  "}
    

@user_router.put("/editar_usuario")
async def update_password(user_schema: UserUpdateSchema, session = Depends(pegar_sessao)):
    user = session.query(User).filter(User.email == user_schema.current_email).first()
    if not user:
        raise HTTPException(status_code=404, detail = "Usuário não encontrado")
    
    if user_schema.new_password is not None:
     user.password = user_schema.new_password

    if user_schema.new_name is not None:
       user.username = user_schema.new_name

    if user_schema.new_email is not None:
       user.email = user_schema.new_email

    session.commit()
    return{"mensagem" : "usuário editado com sucesso  "}
    

@user_router.delete("/excluir_usuario")
async def delete_user(user_schema: UserSchema, session = Depends(pegar_sessao)):
    user = session.query(User).filter(User.email== user_schema.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    else:
        session.delete(user)
        session.commit()
        return {"mensagem" : "usuário excluído com sucesso  "}
    
@user_router.post("/login_usuario")
async def login_user(user_schema: UserSchema, session = Depends(pegar_sessao)):
   ...




   


