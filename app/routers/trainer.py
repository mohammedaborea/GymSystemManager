from app.database import get_db
from app.models import User,Trainer
from fastapi import APIRouter,Depends,HTTPException,Response,status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.schema import UserResp,UserCreate,TrainerResp,TrainerModify,TrainerCreate,UserStatus
from typing import List,Annotated
from app.oauth2 import get_password_hash,get_current_user,trainer_required

router = APIRouter(prefix="/trainer",tags=["trainers"])
@router.get("/",response_model=List[TrainerResp])
def get_trainers(db : Annotated[Session,Depends(get_db)]) :
    trainers = db.query(Trainer).all()
    return trainers


@router.get("/search", response_model=TrainerResp)
def get_trainer(
    db: Annotated[Session, Depends(get_db)],
    phone_num: int | None = None,
    full_name: str | None = None,
    status : UserStatus | None = None
):
    if phone_num is not None:
        trainer = (
            db.query(Trainer)
            .filter(
                Trainer.user.has(User.phone_number == phone_num)
            )
            .first()
        )
    elif full_name is not None:
        trainer = (
            db.query(Trainer)
            .filter(
                Trainer.user.has(User.full_name.contains(full_name))
            )
            .first()
        )
    elif status is not None :
        trainer = (
                    db.query(Trainer)
                    .filter(
                        Trainer.user.has(User.status == status )
                    )
                    .first()
                )
    else:
        raise HTTPException(
            status_code=400,
            detail="Provide phone_num or full_name"
        )

    if not trainer:
        raise HTTPException(
            status_code=404,
            detail="Trainer not found"
        )

    return trainer

@router.post("/")
def add_trainer(db : Annotated[Session,Depends(get_db)] ,response : Response, trainer : TrainerCreate) : 
    trainer_verify = db.query(User).filter(User.email == trainer.email).first()
    if trainer_verify:
        raise HTTPException(404,"Email linked with another account")
    
    new_user = User(full_name = trainer.full_name , email = trainer.email , 
                    phone_number = trainer.phone_number
                    ,role_id = 3,notes = trainer.notes)
    db.add(new_user)   
    db.commit()
    new_trainer = Trainer(user_id = new_user.id , hire_date = trainer.hire_date)
    db.add(new_trainer)
    db.commit()
    response.status_code = status.HTTP_201_CREATED
    return {"message" : "Account created successfully"}
    
    
@router.patch("/{id}",response_model=TrainerResp)
def modify_trainer(id : int ,trainer_data : TrainerModify, db : Annotated[Session,Depends(get_db)]) :
    current_user = db.query(User).filter(User.id == id).first()
    current_trainer = db.query(Trainer).filter(Trainer.user_id == id).first()
    if current_user and current_trainer :
        if trainer_data.full_name is not None :
            current_user.full_name = trainer_data.full_name
        if trainer_data.email is not None :
            current_user.email = trainer_data.email 
        if trainer_data.notes is not None : 
            current_user.notes = trainer_data.notes 
        if trainer_data.phone_number is not None :
            current_user.phone_number = trainer_data.phone_number
        if trainer_data.hire_date is not None :
            current_trainer.hire_date = trainer_data.hire_date
        if trainer_data.monthly_salary is not None :
            current_trainer.monthly_salary = trainer_data.monthly_salary
        if trainer_data.status is not None :
            current_user.status = trainer_data.status
        
        
        db.commit()
        db.refresh(current_trainer)
        return current_trainer
    raise HTTPException(404,"user does not exist")

@router.delete("/{id}")
def delete_trainer(id : int , db : Annotated[Session , Depends(get_db)]) :
    trainer_verify = db.query(Trainer).filter(Trainer.user_id==id)
    user_verify = db.query(User).filter(User.id == id)
    if trainer_verify.first() and user_verify.first() : 
        trainer_verify = trainer_verify.delete()
        user_verify = user_verify.delete()
        db.commit()
        return {"message" : "Account deleted successfully"}

    raise HTTPException(404,"the user does not exist")
    


