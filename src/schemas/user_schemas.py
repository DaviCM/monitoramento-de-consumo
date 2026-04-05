from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSchema(BaseModel):
    real_name: str
    username: str
    email: EmailStr
    password: str



class UpdateUserSchema(BaseModel):
    id: int
    new_name: Optional[str]
    new_email: Optional[EmailStr]
    new_password: Optional[str]



class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    


class Token(BaseModel):
    acess_token: str
    token_type: str
