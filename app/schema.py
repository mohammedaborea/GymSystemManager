from pydantic import BaseModel,EmailStr,ConfigDict
from enum import Enum




class UserBase(BaseModel) : 
    full_name :str
    email : EmailStr
    password : str
    role : str

class UserResp(BaseModel) : 
    full_name : str 
    email : EmailStr

class UserCreate(UserResp) :
    password : str

class TrainerResp(BaseModel) :
    user : UserResp
    bio : str | None = None
    experience : str | None = None
    model_config = ConfigDict(from_attributes=True)


class TrainerModify(BaseModel) :
    full_name : str  | None = None
    email : EmailStr  | None = None
    bio : str  | None = None
    experience : str  | None = None
    



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id : int

class Role(str , Enum) :
    member = "member"
    trainer = "trainer"
    admin = "admin"

class RoleUpdate(BaseModel) :
    role : Role

class passwordChange(BaseModel) : 
    current_password : str
    new_password : str