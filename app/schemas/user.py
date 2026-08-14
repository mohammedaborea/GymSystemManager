from pydantic import BaseModel,EmailStr
from datetime import date
from enum import Enum

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