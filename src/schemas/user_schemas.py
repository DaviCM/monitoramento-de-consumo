from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    username: str
    email: str
    password: str
    real_name: str

class UserUpdateSchema(BaseModel):
    current_email: str | None
    new_name: Optional [str] = None
    new_email: Optional [str] = None
    new_password: Optional [str] = None
