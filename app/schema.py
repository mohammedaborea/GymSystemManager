from pydantic import BaseModel,EmailStr,ConfigDict,model_validator,Field
from enum import Enum
from datetime import date,time , timedelta

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"

class MonthVerify(BaseModel) :
    month: int = Field(ge=1, le=12)
        

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

class ScheduleCreate(BaseModel):
    trainer: str
    date_schedule: date = Field(default_factory=date.today)
    start_time: time
    end_time: time
    zone: str | None = None
    notes: str | None = None

    @model_validator(mode="after")
    def validate_times(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")

        return self

class WeeklyScheduleSearch(BaseModel):
    date_week: date = Field(default_factory=date.today)



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

class ScheduleUpdate(BaseModel) :
    trainer_id : int | None = None
    date_schedule : date | None = None
    start_time: time | None = None
    end_time: time | None = None
    zone: str | None = None
    notes: str | None = None
    model_config = ConfigDict(from_attributes=True)

    
