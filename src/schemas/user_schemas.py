from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class UserSchema(BaseModel):
    real_name: str
    username: str
    email: EmailStr
    password: str



class UpdateUserSchema(BaseModel):
    new_real_name: Optional[str]
    new_username: Optional[str]
    new_email: Optional[EmailStr]
    new_password: Optional[str]



class ResponseUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    real_name: str
    username: str
    email: EmailStr


class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    


    
