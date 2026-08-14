from app.database import get_db
from app.models import User,Trainer
from fastapi import APIRouter,Depends,HTTPException,Response,status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.schemas.common import StandardResponse,ErrorResponse
from app.schemas.trainer import TrainerCreate , TrainerModify , TrainerResp
from app.schemas.user import UserStatus
from typing import List,Annotated


router = APIRouter(prefix="/trainer",tags=["trainers"])
@router.get("/",response_model=StandardResponse[list[TrainerResp]])
def get_trainers(db : Annotated[Session,Depends(get_db)] , limit : int = 10 , skip : int = 0) :
    trainers = db.query(Trainer).limit(limit).offset(skip).all()
    return StandardResponse(success = True ,
                            data = trainers ,
                            message = "Trainer s profile",
                            Error = None)


@router.get("/search", response_model=StandardResponse[TrainerResp])
def get_trainer(
    db: Annotated[Session, Depends(get_db)],
    response : Response ,
    phone_num: int | None = None,
    full_name: str | None = None,
    status_user : UserStatus | None = None
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
    elif status_user is not None :
        trainer = (
                    db.query(Trainer)
                    .filter(
                        Trainer.user.has(User.status == status_user )
                    )
                    .first()
                )
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return StandardResponse(success=False , 
                                data = None , 
                                message="Trainer searching is failed",
                                error = ErrorResponse(
                                    code = "MISSING_ARGUMENTS",
                                    message = "Provide phone_num or full_name or status",
                                    field = "phone_num or full_name or status"
                                ))

    if not trainer:
        response.status_code = status.HTTP_404_NOT_FOUND
        return StandardResponse(success=False , 
                                data = None , 
                                message="Trainer searching is failed",
                                error = ErrorResponse(
                                    code = "Non existing Trainer",
                                    message = "Trainer does not exist"
                                    
                                ))

    return StandardResponse(success=True ,
                            data = trainer ,
                            message = "trainer exists",
                            )

@router.post("/" , response_model=StandardResponse[TrainerResp])
def add_trainer(db : Annotated[Session,Depends(get_db)] ,response : Response, trainer : TrainerCreate) : 
    trainer_verify = db.query(User).filter(User.email == trainer.email).first()
    if trainer_verify:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return StandardResponse(success=False , 
                                data = None , 
                                message="Trainer Creation is failed",
                                error = ErrorResponse(
                                    code = "existing Trainer",
                                    message = "Trainer already exists"
                                            ))
    
    new_user = User(full_name = trainer.full_name , email = trainer.email , 
                    phone_number = trainer.phone_number
                    ,role_id = 3,notes = trainer.notes)
    db.add(new_user)   
    db.commit()
    new_trainer = Trainer(user_id = new_user.id , hire_date = trainer.hire_date)
    db.add(new_trainer)
    db.commit()
    response.status_code = status.HTTP_201_CREATED
    return StandardResponse(success=True , 
                            data = new_trainer , 
                            message="Trainer created successfully"
                                    )
    
    
@router.patch("/{id}",response_model=StandardResponse[TrainerResp])
def modify_trainer(id : int ,
                   response : Response,
                   data : TrainerModify,
                   db : Annotated[Session,Depends(get_db)]) :
    current_user = db.query(User).filter(User.id == id).first()
    current_trainer = db.query(Trainer).filter(Trainer.user_id == id).first()
    if current_user and current_trainer :
        user_fields = {"full_name","email","notes","phone_number","status"}
        trainer_fields = {"hire_date" , "monthly_salary"}
        trainer_data = data.model_dump(exclude_unset=True)
        for field,value in trainer_data.items() :
            if field in user_fields : 
                setattr(current_user , field,value)
            else :
                setattr(current_trainer , field , value)

        db.commit()
        db.refresh(current_trainer)
        response.status_code = status.HTTP_202_ACCEPTED
        return StandardResponse(success=False , 
                                data = current_trainer , 
                                message="Trainer Modified successfully"
                                        )
    response.status_code = status.HTTP_404_NOT_FOUND
    return StandardResponse(success=False , 
                            data = None , 
                            message="Trainer Modifying is failed",
                            error = ErrorResponse(
                                code = "NON_EXISTING_TRAINER",
                                message = "Trainer does not exist"
                                                ))

@router.delete("/{id}" , response_model=StandardResponse[TrainerResp])
def delete_trainer(id : int ,
                   response : Response ,
                   db : Annotated[Session , Depends(get_db)]) :
    trainer_verify = db.query(Trainer).filter(Trainer.user_id==id)
    user_verify = db.query(User).filter(User.id == id)
    if trainer_verify.first() and user_verify.first() : 
        trainer_verify = trainer_verify.delete()
        user_verify = user_verify.delete()
        db.commit()
        response.status_code = status.HTTP_200_OK
        return StandardResponse(success=True , 
                                data = None , 
                                message="Trainer Deleting Successfully"
                                        )

    response.status_code = status.HTTP_404_NOT_FOUND
    return StandardResponse(success=False , 
                            data = None , 
                            message="Trainer Deleting is failed",
                            error = ErrorResponse(
                            code = "NON_EXISTING_TRAINER",
                            message = "Trainer does not exist"
                                                ))
    


