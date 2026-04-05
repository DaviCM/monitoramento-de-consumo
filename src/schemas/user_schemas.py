from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSchema(BaseModel):
    
    real_name: str
    username: str
    email: EmailStr
    password: str



class UpdateUserSchema(BaseModel):
    id: int
    new_name: Optional[str] = None
    new_email: Optional[EmailStr] = None
    new_password: Optional[str] = None



class Token(BaseModel):
    access_token: str
    token_type: str



class ForgotPasswordSchema(BaseModel):
    email: str
    new_password: str