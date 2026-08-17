from pydantic import BaseModel ,ConfigDict,EmailStr,Field,model_validator
from datetime import date,time



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