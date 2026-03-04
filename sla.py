from models.usuario import User
from passlib.hash import pbkdf2_sha256
from fastapi import FastAPI

app = FastAPI

class User(Base):

 @app.post("/usuarios")
 def cadastro_usuario():
    ...

 @app.put
 def editar_usuario():
   ...
 
 @app.patch
 def editar_algo_especifico():
   ...
   
