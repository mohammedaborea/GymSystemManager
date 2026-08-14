from app.database import get_db
from app.models import User,Member,Membership
from fastapi import APIRouter,Depends,HTTPException,Response,status,Query

from sqlalchemy.orm import Session,selectinload
from app.schema import MembershipCreate,MembershipModify
from typing import List,Annotated
from collections import defaultdict
from datetime import date,timedelta

router = APIRouter(prefix="/membership" , tags=["memberships"])

@router.post("/")
def add_membership(db : Annotated[Session , Depends(get_db)] , membership : MembershipCreate) :
    membership_verify = db.query(Membership).filter(Membership.name == membership.name).first()
    if not membership_verify :
        new_mem = Membership(name = membership.name)
        db.add(new_mem)
        db.commit()
        return {"message" : "Membership added successfully"}
    raise HTTPException(404 , "Membership already exist")

@router.get("/",response_model=List[MembershipCreate])
def get_membership(db : Annotated[Session , Depends(get_db)],limit : int = 10 , skip : int = 0 ) :
   
    memberships = db.query(Membership).limit(limit).offset(skip).all()
    
    return memberships


@router.delete("/{id}")
def delete_membership(id : int ,db : Annotated[Session , Depends(get_db)]) :
    membership_verify = db.query(Membership).filter(Membership.id == id)
    if membership_verify.first() :
        membership_verify = membership_verify.delete(synchronize_session=False)
        db.commit()
        
        return {"message":"membership deleted successfully"}
    raise HTTPException(404 , "Membership not found")

@router.patch("/{id}")
def modify_membership(id : int ,db : Annotated[Session , Depends(get_db)] , data : MembershipModify) :
    membership_verify = db.query(Membership).filter(Membership.id == id).first()
    if membership_verify:
        membership = data.model_dump(exclude_unset=True)
        for field , value in membership.items() :
            setattr(membership_verify , field , value)
        db.commit()
        db.refresh(membership_verify)
        return membership_verify
    raise HTTPException(404 , "Membership not found")


@router.get("/search")
def get_memb(db : Annotated[Session , Depends(get_db)] , pseudo : str) :
    membership_verify = db.query(Membership).filter(Membership.name.contains(pseudo)).first()
    if membership_verify : 
        return membership_verify
    raise HTTPException(404 , "Membership not found")
    



    


