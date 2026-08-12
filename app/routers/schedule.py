from app.database import get_db
from app.models import User,Trainer,Schedule
from fastapi import APIRouter,Depends,HTTPException,Response,status,Query
from sqlalchemy import select,extract
from sqlalchemy.orm import Session
from app.schema import UserResp,UserCreate,TrainerResp,TrainerModify,TrainerCreate,ScheduleUpdate,UserStatus,ScheduleCreate,MonthVerify,WeeklyScheduleSearch
from typing import List,Annotated
from collections import defaultdict
from datetime import date,timedelta
from calendar import monthrange

router = APIRouter(prefix="/schedule",tags=["schedules"])

@router.post("/")
def add_schedule(response : Response,db : Annotated[Session , Depends(get_db)],schedule : ScheduleCreate) :
    trainer_verify = db.query(Trainer).filter(Trainer.user.has(User.full_name.contains(schedule.trainer))).first()
    if trainer_verify : 
        new_schedule = Schedule(trainer_id = trainer_verify.user_id , date_schedule = schedule.date_schedule , zone = schedule.zone , 
                                start_time = schedule.start_time , end_time = schedule.end_time , notes = schedule.notes)
        db.add(new_schedule)
        db.commit()
        db.refresh(new_schedule)
        response.status_code = status.HTTP_201_CREATED
        return new_schedule
    raise HTTPException(404,"trainer is not found")

@router.get("/monthly")
def get_schedule_by_month(month : int , year : int, db : Annotated[Session , Depends(get_db)]) : 

    first_day = date(year,month,1)
    last_day = date(year , month , monthrange(year,month)[1])
    schedules = db.query(Schedule).filter(Schedule.date_schedule >= first_day,Schedule.date_schedule<=last_day).order_by(Schedule.date_schedule, Schedule.start_time).all()
    

    grouped = defaultdict(list)
    

    for schedule in schedules:
        grouped[schedule.date_schedule.day].append(schedule)
    return grouped


@router.delete("/{id}")
def delete_schedule(id : int , response : Response ,db : Annotated[Session , Depends(get_db)],trainer : str | None = None):
    
    schedule_verify = db.query(Schedule).filter(Schedule.id == id)
    if schedule_verify.first() :
        schedule_verify = schedule_verify.delete(synchronize_session=False)
        response.status_code = status.HTTP_204_NO_CONTENT
        db.commit()
        return {"message" : "Schedule deleted successfully"}
    raise HTTPException(404,"Schedule does not exist")

@router.get("/weekly")
def get_schedule_byweek(search: Annotated[WeeklyScheduleSearch, Query()],db : Annotated[Session , Depends(get_db)]) :
    requested_date = search.date_week 

    start_of_week = requested_date - timedelta(days=requested_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    schedules = db.query(Schedule).filter(Schedule.date_schedule >= start_of_week,Schedule.date_schedule<=end_of_week).order_by(Schedule.date_schedule, Schedule.start_time).all()
        
    
    grouped = defaultdict(list)
        
    
    for schedule in schedules:
        grouped[schedule.date_schedule.day].append(schedule)
    return grouped

@router.get("/")
def get_schedules(db : Annotated[Session , Depends(get_db)]) :
    trainers = db.query(Trainer).all()
    schedules = defaultdict(list)
    for trainer in trainers :
        for schedule in trainer.schedules :
            schedules[trainer.user.full_name].append(schedule)
    return schedules
            
@router.patch("/{id}")
def update_schedule(id : int,data : ScheduleUpdate ,db : Annotated[Session , Depends(get_db)]) :
    
    schedule_verify = db.query(Schedule).filter(Schedule.id == id).first()
    if schedule_verify :
        update_sch = data.model_dump(exclude_unset=True)
        for field,value in update_sch.items() :
            setattr(schedule_verify,field,value)
        db.commit()
        db.refresh(schedule_verify)
        return schedule_verify
    raise HTTPException(404,"Schedule not found")




