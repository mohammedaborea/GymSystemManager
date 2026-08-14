from pydantic import BaseModel ,ConfigDict,EmailStr
from datetime import date
from .user import UserBase,UserResp,UserStatus

class MemberResp(BaseModel) :
    user : UserResp
    member_id : int
    joined_at : date | None = None
    expiry_date : date | None = None
    model_config = ConfigDict(from_attributes=True)
    
class MemberCreate(UserBase) :
    joined_at : date | None = None
    expiry_date : date | None = None
    fitness_goal_id : int 
    membership_id : int


class MemberModify(BaseModel) :
    full_name :str | None = None
    email : EmailStr | None = None
    phone_number : int | None = None
    status : UserStatus | None = None
    notes : str | None = None
    joined_at : date | None = None
    expiry_date : date | None = None
    fitness_goal_id : int | None = None
    membership_id : int | None = None 