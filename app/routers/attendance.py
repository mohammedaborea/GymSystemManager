from app.database import get_db
from app.models import User,Trainer,Attendance,MarkAttendance
from fastapi import APIRouter,Depends,HTTPException,Response,status,Query

from sqlalchemy.orm import Session,selectinload
from app.schema import TrainerCreate,TrainerModify,TrainerResp,AttendanceCreate,AttendanceResp,AttendanceModify
from typing import List,Annotated
from collections import defaultdict
from datetime import date,timedelta

router = APIRouter(prefix="/attendance" , tags=["attendances"])

@router.post("/", response_model=AttendanceResp)
def mark_attendance(attendance : AttendanceCreate ,db : Annotated[Session , Depends(get_db)]) :
    attendance_verify = db.query(MarkAttendance).filter(MarkAttendance.trainer_id == attendance.trainer_id, MarkAttendance.date_att == attendance.date_att).first()
    if not attendance_verify :
        new_att = MarkAttendance(trainer_id = attendance.trainer_id , attendance_id = attendance.attendance_id ,
                                 check_in = attendance.check_in , check_out = attendance.check_out , notes = attendance.notes,
                                 date_att = attendance.date_att)
        db.add(new_att)
        db.commit()
        db.refresh(new_att)
        return {
            "full_name" : new_att.trainer.user.full_name,
            "status" : new_att.attendance.status ,
            "date_att" : new_att.date_att,
            "check_in" : new_att.check_in,
            "check_out" : new_att.check_out
            
        }
    raise HTTPException(404,"Attendance already exist")



@router.get("/", response_model=List[AttendanceResp])
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

    return result

@router.delete("/{trainer_id}")
def delete_attendance(trainer_id : int,db : Annotated[Session , Depends(get_db)],date_att : Annotated[date, Query()] = date.today()) :
    attendance_verify = db.query(MarkAttendance).filter(MarkAttendance.trainer_id == trainer_id, 
                                                        MarkAttendance.date_att == date_att)
    if attendance_verify.first() :
        attendance_verify = attendance_verify.delete(synchronize_session=False)
        db.commit()
        return {"message" : "Attendance record is deleted successfully"}
    raise HTTPException(404,"Attendance record not found")

@router.patch("/{trainer_id}",response_model=AttendanceResp)
def modify_attendance(trainer_id : int,db : Annotated[Session , Depends(get_db)],
                      data : AttendanceModify) :
    attendance_verify = db.query(MarkAttendance).filter(MarkAttendance.trainer_id == trainer_id, 
                                                            MarkAttendance.date_att == data.date_att).first()
    if attendance_verify :
        attendances_rec = data.model_dump(exclude_unset=True)
        for field,value in attendances_rec.items() :
            setattr(attendance_verify,field,value)
        
        db.commit()
        db.refresh(attendance_verify)
        return {
            "full_name" : attendance_verify.trainer.user.full_name,
            "status" : attendance_verify.attendance.status ,
            "date_att" : attendance_verify.date_att,
            "check_in" : attendance_verify.check_in,
            "check_out" : attendance_verify.check_out
            
        }
    

@router.get("/trainer/{id}")
def get_trainer_recs(id : int,db : Annotated[Session , Depends(get_db)],date_att : Annotated[date,Query()] = date.today()) :
    trainer_verify = db.query(Trainer).filter(Trainer.user_id == id).first()
    if trainer_verify :
        rec = db.query(MarkAttendance).filter(MarkAttendance.trainer_id == id , MarkAttendance.date_att == date_att).first()
        
        return {"full_name" : rec.trainer.user.full_name,
                "status" : rec.attendance.status ,
                "date_att" : rec.date_att,
                "check_in" : rec.check_in,
                "check_out" : rec.check_out}
                    
          
    raise HTTPException(404,"Trainer not found")


