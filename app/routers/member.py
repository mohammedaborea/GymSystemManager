from app.database import get_db
from app.models import User,Member
from fastapi import APIRouter,Depends,HTTPException,Response,status,Query

from sqlalchemy.orm import Session
from app.schema import MemberResp,MemberCreate,UserStatus,MemberModify
from typing import List,Annotated
from collections import defaultdict
from datetime import date,timedelta

router = APIRouter(prefix="/member" , tags=["members"])

@router.get("/",response_model=List[MemberResp])
def get_members(db : Annotated[Session , Depends(get_db)] , limit : int = 10 , skip : int = 0) :
    members = db.query(Member).limit(limit).offset(skip).all()
    return members

@router.post("/")
def add_member(db : Annotated[Session , Depends(get_db)],response : Response , member : MemberCreate) :
    user_verify = db.query(User).filter(User.phone_number == member.phone_number).first()
    if user_verify : 
        raise HTTPException(404,"User already exists")
    new_user = User(email = member.email , phone_number = member.phone_number,full_name = member.full_name,status = member.status,
                    notes = member.notes , role_id = 1)
    db.add(new_user)
    db.commit()
    new_member = Member(member_id = new_user.id,joined_at = member.joined_at,expiry_date = member.expiry_date ,fitness_goal_id = member.fitness_goal_id,
                        membership_id = member.membership_id )
    db.add(new_member)
    db.commit()
    response.status_code = status.HTTP_201_CREATED
    return {"message" : "Member Created Successfully"}


@router.delete("/{id}")
def delete_trainer(id : int , db : Annotated[Session , Depends(get_db)]) :
    member_verify = db.query(Member).filter(Member.member_id==id)
    user_verify = db.query(User).filter(User.id == id)
    if member_verify.first() and user_verify.first() : 
        member_verify = member_verify.delete()
        user_verify = user_verify.delete()
        db.commit()
        return {"message" : "Account deleted successfully"}

    raise HTTPException(404,"the user does not exist")

@router.get("/search", response_model=MemberResp)
def get_member(
    db: Annotated[Session, Depends(get_db)],
    phone_num: int | None = None,
    full_name: str | None = None,
    status : UserStatus | None = None
):
    if phone_num is not None:
        member = (
            db.query(Member)
            .filter(
                Member.user.has(User.phone_number == phone_num)
            )
            .first()
        )
    elif full_name is not None:
        member = (
            db.query(Member)
            .filter(
                Member.user.has(User.full_name.contains(full_name))
            )
            .first()
        )
    elif status is not None :
        member = (
                    db.query(Member)
                    .filter(
                        Member.user.has(User.status == status )
                    )
                    .first()
                )
    else:
        raise HTTPException(
            status_code=400,
            detail="Provide phone_num or full_name or status"
        )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    return member

@router.patch("/{id}",response_model=MemberResp)
def modify_member(id : int ,data : MemberModify , db : Annotated[Session , Depends(get_db)]) :
    
    member_verify = db.query(Member).filter(Member.member_id == id).first()
    if member_verify :
        user_fields = {"full_name" , "email" , "phone_number" , "status" , "notes"}
        member_fields = {"joined_at" , "expiry_date" , "fitness_goal_id" , "membership_id"}
        member = data.model_dump(exclude_unset=True)
        for field,value in member.items() :
            if field in user_fields :
                setattr(member_verify.user,field,value)
            else :
                setattr(member_verify,field,value)
        db.commit()
        db.refresh(member_verify)
        return member_verify
    raise HTTPException(404,"Member Not Found")
