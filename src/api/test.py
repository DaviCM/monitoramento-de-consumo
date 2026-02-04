from fastapi import FastAPI, status, HTTPException, APIRouter
from http import HTTPStatus
from pydantic import BaseModel, EmailStr
from typing import Any
# Quando a controllers estiver pronta, importar ela


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None



class UserIn(BaseUser):
    password:str



router = APIRouter()
user_controller = user_Controller() #Alterar depois quando a controller estiver pronta

@router.post(
        "/user/{user_id}", 
        status_code=status.HTTP_201_CREATED
        responde_model= UserOut)
async def create_user(user_id: str , user: UserIn) ->  UserOut:
  try:
    user_created = user_controller.create_user(user_id, user.dict())
    return user_created # Pegar da controller
  except ValueError as e:
     raise HTTPException(status_code=404, detail= str(e))
  

@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def drop_user():
    try:
      user_deleted = user_controller.delete_user(user_id,())
      return 
    except:
     raise HTTPException(status_code=404, detail="Não encontrado")
    
   
@router.put("/recurso/{user_id}", response_model=RecursoOut)
async def update_user(id: int, dados: RecursosIn):
    try:
        user_updated = user_controller.update_user(user_id, user.dict())
        return user_updated(id, dados)
    except
    if user not user_updated:
     raise  HTTPException(status_code=404, detail="Não encontrado")
    

@router.put ("/simulacao_consumo/{consumption_id}", response_model= ConsumoOut)
async def consumption_simulation(id: int, dados: ConsumoIn):
    ...

@router
async def consumption_history():
    ...
@router
async def drop_consumption():
    ...

@router
async def update_information_of_consumption():
    ...
@router
async def goal_model():
    ...
@router
async def tip_model():
    ...
@router
async def len_consumption():
    ...
@router 
async def new_tip():
    ...
@router 
async def randon_tip():
    ...

@router
async def selection_tip():
    ...

@router
async def drop_tip():
    ...
