from pydantic import BaseModel, ConfigDict

class ResponseTokensSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    access_token: str
    refresh_token: str
    token_type: str
    

class ResponseAccessTokenSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    access_token: str
    token_type: str
    
    