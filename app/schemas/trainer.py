from pydantic import BaseModel,ConfigDict,EmailStr
from datetime import date
from .user import UserBase,UserResp,UserStatus

class TrainerResp(BaseModel) :
    user : UserResp
    id : int
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
