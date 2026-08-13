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


class AttendanceCreate(BaseModel) :
    trainer_id : int 
    attendance_id : int
    date_att : date = Field(default_factory=date.today)
    check_in  : time 
    check_out : time
    notes : str | None = None

    @model_validator(mode="after")
    def validate_times(self):

        if self.check_out <= self.check_in:
            raise ValueError("check_out must be after check_in")
    
        return self

class AttendanceResp(BaseModel) :
    full_name : str 
    status : str             
    check_in : time 
    check_out : time
    date_att : date
    notes : str | None = None

class AttendanceModify(BaseModel) :
    
    date_att : date = Field(default_factory=date.today)
    check_in  : time | None = None
    check_out : time | None = None
    notes : str | None = None
    
    

    
