from app.database import get_db
from app.models import User,Trainer,Schedule
from fastapi import APIRouter,Depends,HTTPException,Response,status,Query
from sqlalchemy import select,extract
from sqlalchemy.orm import Session
from app.schemas.schedule import ScheduleUpdate,ScheduleCreate,WeeklyScheduleSearch,ScheduleResponse
from app.schemas.common import ErrorResponse , StandardResponse
from typing import List,Annotated
from collections import defaultdict
from datetime import date,timedelta
from calendar import monthrange
from app.oauth2 import get_current_user
router = APIRouter(prefix="/schedule",tags=["schedules"],dependencies=[Depends(get_current_user)])

@router.post("/" , response_model=StandardResponse[ScheduleResponse])
def add_schedule(response : Response,db : Annotated[Session , Depends(get_db)],schedule : ScheduleCreate) :
    trainer_verify = db.query(Trainer).filter(Trainer.id == schedule.trainer_id).first()
    if trainer_verify : 
        new_schedule = Schedule(trainer_id = schedule.trainer_id , date_schedule = schedule.date_schedule , zone = schedule.zone , 
                                start_time = schedule.start_time , end_time = schedule.end_time , notes = schedule.notes)
        db.add(new_schedule)
        db.commit()
        db.refresh(new_schedule)
        response.status_code = status.HTTP_201_CREATED
        return StandardResponse(
            success = True , 
            data = new_schedule , 
            message = "Schedule Created Successfully"
            
        )
    response.status_code = status.HTTP_404_NOT_FOUND
    return StandardResponse(
        success = False , 
        data = None , 
        message = "Schedule Creation is Failed " ,
        error = ErrorResponse(
            code = "NON_EXISTING_TRAINER" , 
            message="Trainer does not exist" ,

        )
    )

@router.get("/monthly",response_model=StandardResponse[dict[int,List[ScheduleResponse]]])
def get_schedule_by_month(response : Response,db : Annotated[Session , Depends(get_db)],month : int | None = None , year : int | None = None) : 
    if month is None :
        month = date.today().month
    if year is None :
        year = date.today().year

    if not (1<=month<=12 and 2000<=year<=9999) :
        response.status_code = status.HTTP_400_BAD_REQUEST
        return StandardResponse(
            success= False , 
            data = None ,
            message="Error in the arguments provided by the user" , 
            error =ErrorResponse (
                code = "MISSING_ARGUMENTS",
                message="Please check the validation of the arguments" ,
                field = "Month or Year"
            )
        )
    
    first_day = date(year,month,1)
    last_day = date(year , month , monthrange(year,month)[1])
    schedules = db.query(Schedule).filter(Schedule.date_schedule >= first_day,Schedule.date_schedule<=last_day).order_by(Schedule.date_schedule, Schedule.start_time).all()
    

    grouped = defaultdict(list)
    

    for schedule in schedules:
        grouped[schedule.date_schedule.day].append(schedule)

    
    return StandardResponse(
        success=True , 
        data = grouped, 
        message = "Schedules obtained successfully"
    )


@router.delete("/{id}",response_model=StandardResponse[ScheduleCreate])
def delete_schedule(id : int , response : Response ,db : Annotated[Session , Depends(get_db)],trainer : str | None = None):
    
    schedule_verify = db.query(Schedule).filter(Schedule.id == id)
    if schedule_verify.first() :
        schedule_verify = schedule_verify.delete(synchronize_session=False)
        db.commit()
        return StandardResponse(
            success = True , 
            message = "Schedule deleted successfully",
            data=None
        )
    response.status_code = status.HTTP_404_NOT_FOUND
    return StandardResponse(
        success=False , 
        data=None ,
        message = "Schedule deleting is failed",
        error=ErrorResponse(
            code = "NON_EXISTING_SCHEDULE",
            message="Schedule does not exist"
        )
    )

@router.get("/weekly",response_model=StandardResponse[dict[int,List[ScheduleCreate]]])
def get_schedule_byweek(search: Annotated[WeeklyScheduleSearch, Query()],db : Annotated[Session , Depends(get_db)]) :
    requested_date = search.date_week 

    start_of_week = requested_date - timedelta(days=requested_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    schedules = db.query(Schedule).filter(Schedule.date_schedule >= start_of_week,Schedule.date_schedule<=end_of_week).order_by(Schedule.date_schedule, Schedule.start_time).all()
        
    
    grouped = defaultdict(list)
        
    
    for schedule in schedules:
        grouped[schedule.date_schedule.day].append(schedule)
    return StandardResponse(
            success=True , 
            data = grouped, 
            message = "Schedules obtained successfully"
        )


            
@router.patch("/{id}" , response_model=StandardResponse[ScheduleResponse])
def update_schedule(id : int,response : Response,data : ScheduleUpdate ,db : Annotated[Session , Depends(get_db)]) :
    
    schedule_verify = db.query(Schedule).filter(Schedule.id == id).first()
    if schedule_verify :
        update_sch = data.model_dump(exclude_unset=True)
        for field,value in update_sch.items() :
            setattr(schedule_verify,field,value)
        db.commit()
        db.refresh(schedule_verify)
        return StandardResponse(
                success=True , 
                data = schedule_verify , 
                message = "Schedules updated successfully"
            )
    response.status_code = status.HTTP_404_NOT_FOUND
    return StandardResponse(
            success=False , 
            data=None ,
            message = "Schedule updating is failed",
            error=ErrorResponse(
                code = "NON_EXISTING_SCHEDULE",
                message="Schedule does not exist"
            )
        )




