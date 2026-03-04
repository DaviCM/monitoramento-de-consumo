from pydantic import BaseModel
# from typing import Optional

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    real_name: str

class UserUpdateSchema(BaseModel):
    current_email: str
    new_name: str
    new_email: str
    new_password: str


