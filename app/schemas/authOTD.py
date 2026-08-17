from pydantic import BaseModel,EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id : int

class AdminCreate(BaseModel) :
    email :EmailStr
    password:str

class AdminResponse(BaseModel) : 
    id : int 
    email : EmailStr