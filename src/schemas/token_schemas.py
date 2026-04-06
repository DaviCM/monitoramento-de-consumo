from pydantic import BaseModel, ConfigDict

class AccessTokenSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    access_token: str
    token_type: str
    
    