from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, SecretStr, ConfigDict

class UserSchema(BaseModel):
    real_name: str
    username: str
    email: EmailStr
    password: SecretStr
    
    
    
class LoginUserSchema(BaseModel):
    email: EmailStr
    password: SecretStr



class UpdateUserSchema(BaseModel):
    new_real_name: Optional[str]
    new_username: Optional[str]
    new_email: Optional[EmailStr]
    new_password: Optional[SecretStr]



class ResponseUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    real_name: str
    username: str
    email: EmailStr
    created_at: datetime



class ForgottenPasswordSchema(BaseModel):
    email: EmailStr
    


class PasswordRecoverySchema(BaseModel):
    new_password: SecretStr
    recovery_token: str
    
    

class RefreshTokenSchema(BaseModel):
    refresh_token: str


    
