from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: int
    real_name: str
    username: str
    email: str
    password: str



class UpdateUserSchema(BaseModel):
    id: int
    new_name: Optional[str] = None
    new_email: Optional[str] = None
    new_password: Optional[str] = None
