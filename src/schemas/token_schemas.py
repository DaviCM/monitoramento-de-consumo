from pydantic import BaseModel

class Token(BaseModel):
    acess_token: str
    token_type: str
    
    