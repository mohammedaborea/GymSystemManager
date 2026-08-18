from pydantic import BaseModel , EmailStr , ConfigDict , Field , model_validator
from datetime import date,time


class ScheduleUpdate(BaseModel) :
    trainer_id : int | None = None
    date_schedule : date | None = None
    start_time: time | None = None
    end_time: time | None = None
    zone: str | None = None
    notes: str | None = None
    model_config = ConfigDict(from_attributes=True)

class ScheduleCreate(BaseModel):
    trainer_id: int
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

class ScheduleResponse(BaseModel) :
    id : int
    date_schedule: date
    start_time : time
    end_time : time
    zone: str | None = None
    notes: str | None = None
    model_config = ConfigDict(from_attributes=True)
    

class WeeklyScheduleSearch(BaseModel):
    date_week: date = Field(default_factory=date.today)