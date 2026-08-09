from app.database import get_db
from app.models import User,Trainer
from fastapi import APIRouter,Depends,HTTPException,Response,status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.schema import UserResp,UserCreate,TrainerResp,TrainerModify
from typing import List,Annotated
from app.oauth2 import get_password_hash,get_current_user,trainer_required

router = APIRouter(prefix="/trainer",tags=["trainers"])
@router.get("/",response_model=List[TrainerResp])
def get_trainers(db : Annotated[Session,Depends(get_db)]) :
    trainers = db.query(Trainer).all()
    return trainers


@router.get("/{id}",response_model=TrainerResp)
def get_trainer(id : int , db : Annotated[Session,Depends(get_db)]) :
    trainer=db.query(Trainer).filter(Trainer.user_id == id).first()
    if not trainer :
        raise HTTPException(404,"Trainer not found")
    
    
    return trainer


@router.patch("/me",response_model=TrainerResp)
def modify_trainer(trainer_data : TrainerModify, db : Annotated[Session,Depends(get_db)],trainer = Depends(trainer_required)) :
    current_trainer = db.query(Trainer).filter(Trainer.user_id == trainer.id).first()
    trainer.full_name=trainer_data.full_name
    trainer.email = trainer_data.email
    current_trainer.experience = trainer_data.experience
    current_trainer.bio = trainer_data.bio
    db.commit()
    db.refresh(trainer)
    return trainer
