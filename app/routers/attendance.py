from app.database import get_db
from app.models import User,Trainer,Attendance,MarkAttendance
from fastapi import APIRouter,Depends,HTTPException,Response,status,Query

from sqlalchemy.orm import Session,selectinload
from app.schemas.attendance import AttendanceCreate,AttendanceResp,AttendanceModify
from app.schemas.common import StandardResponse,ErrorResponse
from typing import List,Annotated
from collections import defaultdict
from datetime import date,timedelta
from app.oauth2 import get_current_user

router = APIRouter(prefix="/attendance" , tags=["attendances"],dependencies=[Depends(get_current_user)])

@router.post("/", response_model=StandardResponse[AttendanceResp])
def mark_attendance(attendance : AttendanceCreate,response : Response ,db : Annotated[Session , Depends(get_db)]) :
    attendance_verify = db.query(MarkAttendance).filter(MarkAttendance.trainer_id == attendance.trainer_id, MarkAttendance.date_att == attendance.date_att).first()
    if not attendance_verify :
        new_att = MarkAttendance(trainer_id = attendance.trainer_id , attendance_id = attendance.attendance_id ,
                                 check_in = attendance.check_in , check_out = attendance.check_out , notes = attendance.notes,
                                 date_att = attendance.date_att)
        db.add(new_att)
        db.commit()
        db.refresh(new_att)
        response.status_code =status.HTTP_201_CREATED
        return StandardResponse(
            success = True ,
            data = {
            "full_name" : new_att.trainer.user.full_name,
            "status" : new_att.attendance.status ,
            "date_att" : new_att.date_att,
            "check_in" : new_att.check_in,
            "check_out" : new_att.check_out
            },
            message = "Attendance Created Successfully"
        )

    response.status_code =status.HTTP_400_BAD_REQUEST
    return StandardResponse(
        success=False,
        data= None ,
        message = "Attendance Creation is failed",
        error= ErrorResponse(
            code = "EXISTING ATTENDANCE",
            message="Attendance already exists"
        )
    )



@router.get("/", response_model=StandardResponse[List[AttendanceResp]])
def get_attendance(
    db: Annotated[Session, Depends(get_db)],
    date_att: Annotated[date, Query()] = date.today()
):
    attendances = (
        db.query(MarkAttendance)
        .options(
            selectinload(MarkAttendance.trainer)
            .selectinload(Trainer.user),

            selectinload(MarkAttendance.attendance)
        )
        .filter(MarkAttendance.date_att == date_att)
        .all()
    )

    result = []

    for attendance in attendances:
        result.append({
            "full_name": attendance.trainer.user.full_name,
            "status": attendance.attendance.status,
            "date_att": attendance.date_att,
            "check_in": attendance.check_in,
            "check_out": attendance.check_out
        })

    return StandardResponse(
                success = True ,
                data =result,
                message = "Attendance Obtained Successfully"
            )

@router.delete("/{trainer_id}",response_model=StandardResponse[AttendanceResp])
def delete_attendance(trainer_id : int,response : Response,db : Annotated[Session , Depends(get_db)],date_att : Annotated[date, Query()] = date.today()) :
    attendance_verify = db.query(MarkAttendance).filter(MarkAttendance.trainer_id == trainer_id, 
                                                        MarkAttendance.date_att == date_att)
    if attendance_verify.first() :
        attendance_verify = attendance_verify.delete(synchronize_session=False)
        db.commit()
        return StandardResponse(
                    success = True ,
                    data =None,
                    message = "Attendance Deleted Successfully"
                )
    response.status_code = status.HTTP_404_NOT_FOUND
    return StandardResponse(
            success=False,
            data= None ,
            message = "Attendance Deleting is failed",
            error= ErrorResponse(
                code = "NON EXISTING ATTENDANCE",
                message="Attendance Does not exist"
            )
        )

@router.patch("/{trainer_id}",response_model=StandardResponse[AttendanceResp])
def modify_attendance(trainer_id : int,response : Response,db : Annotated[Session , Depends(get_db)],
                      data : AttendanceModify) :
    attendance_verify = db.query(MarkAttendance).filter(MarkAttendance.trainer_id == trainer_id, 
                                                            MarkAttendance.date_att == data.date_att).first()
    if attendance_verify :
        attendances_rec = data.model_dump(exclude_unset=True)
        for field,value in attendances_rec.items() :
            setattr(attendance_verify,field,value)
        
        db.commit()
        db.refresh(attendance_verify)
        response.status_code = status.HTTP_202_ACCEPTED
        return StandardResponse(
                    success = True ,
                    data = {
                    "full_name" : attendance_verify.trainer.user.full_name,
                    "status" : attendance_verify.attendance.status ,
                    "date_att" : attendance_verify.date_att,
                    "check_in" : attendance_verify.check_in,
                    "check_out" : attendance_verify.check_out
                    },
                    message = "Attendance Modified Successfully"
                )
    response.status_code = status.HTTP_404_NOT_FOUND
    return StandardResponse(
                success=False,
                data= None ,
                message = "Attendance Modifying is failed",
                error= ErrorResponse(
                    code = "NON EXISTING ATTENDANCE",
                    message="Attendance Does not exist"
                )
            )
    

@router.get("/trainer/{id}" , response_model=StandardResponse[AttendanceResp])
def get_trainer_recs(id : int,response : Response,db : Annotated[Session , Depends(get_db)],date_att : Annotated[date,Query()] = date.today()) :
    trainer_verify = db.query(Trainer).filter(Trainer.id == id).first()
    if trainer_verify :
        rec = db.query(MarkAttendance).filter(MarkAttendance.trainer_id == id , MarkAttendance.date_att == date_att).first()
        
        return StandardResponse(
                            success = True ,
                            data = {
                            "full_name" : rec.trainer.user.full_name,
                            "status" : rec.attendance.status ,
                            "date_att" : rec.date_att,
                            "check_in" : rec.check_in,
                            "check_out" : rec.check_out
                            },
                            message = "Attendance Obtained Successfully"
                        )
                    
    response.status_code = status.HTTP_404_NOT_FOUND          
    return StandardResponse(
                    success=False,
                    data= None ,
                    message = "Trainer's recs is failed",
                    error= ErrorResponse(
                        code = "NON EXISTING Trainer",
                        message="Trainer Does not exist"
                    )
                )


