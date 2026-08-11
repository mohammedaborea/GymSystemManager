from pydantic import BaseModel,EmailStr,ConfigDict
from enum import Enum
from datetime import date

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"


class UserBase(BaseModel) : 
    full_name :str
    email : EmailStr
    phone_number : int
    status : UserStatus = UserStatus.ACTIVE
    notes : str

class UserResp(UserBase) : 
    birdthday : date | None = None 

class UserCreate(UserResp) :
    joined_at : date
    expiry_date : date
    fitness_goal : str | None = None
    membership : str 

class TrainerResp(BaseModel) :
    user : UserResp
    user_id : int
    hire_date : date | None = None
    monthly_salary : int | None = None
    model_config = ConfigDict(from_attributes=True)




class TrainerModify(BaseModel) :
    full_name :str | None = None
    email : EmailStr | None = None
    phone_number : int | None = None
    status : UserStatus | None = None
    notes : str | None = None
    monthly_salary : int | None = None
    hire_date : date | None = None
class TrainerCreate(UserBase) :
    monthly_salary : int | None = None
    hire_date : date
    



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