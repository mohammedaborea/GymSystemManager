from app.database import get_db
from app.models import User,Member
from fastapi import APIRouter,Depends,HTTPException,Response,status,Query

from sqlalchemy.orm import Session
from app.schemas.member import MemberResp,MemberCreate,UserStatus,MemberModify
from app.schemas.common import StandardResponse,ErrorResponse
from typing import List,Annotated
from collections import defaultdict
from datetime import date,timedelta
from app.oauth2 import get_current_user

router = APIRouter(prefix="/member" , tags=["members"],dependencies=[Depends(get_current_user)] )

@router.get("/",response_model=StandardResponse[List[MemberResp]])
def get_members(db : Annotated[Session , Depends(get_db)] , limit : int = 10 , skip : int = 0) :
    members = db.query(Member).limit(limit).offset(skip).all()
    return StandardResponse(
                                    success=True , 
                                    data = members ,
                                    message = "Members Obtained Successfully"
                                )

@router.post("/",response_model=StandardResponse[MemberResp])
def add_member(db : Annotated[Session , Depends(get_db)],response : Response , member : MemberCreate) :
    user_verify = db.query(User).filter(User.phone_number == member.phone_number).first()
    if user_verify : 
        response.status_code = status.HTTP_400_BAD_REQUEST
        return StandardResponse(
                                            success=False , 
                                            data = None ,
                                            message = "Member Creation Is Failed",
                                            error = ErrorResponse(
                                                code = "EXISTING MEMBER",
                                                message="Member already exists"
                                            )
                                        )
        
    new_user = User(email = member.email , phone_number = member.phone_number,full_name = member.full_name,status = member.status,
                    notes = member.notes)
    db.add(new_user)
    db.commit()
    new_member = Member(member_id = new_user.id,joined_at = member.joined_at,expiry_date = member.expiry_date ,fitness_goal_id = member.fitness_goal_id,
                        membership_id = member.membership_id )
    db.add(new_member)
    db.commit()
    response.status_code = status.HTTP_201_CREATED
    return StandardResponse(
                                        success=True , 
                                        data = new_member ,
                                        message = "Member Created Successfully"
                                    )
    


@router.delete("/{id}" , response_model=StandardResponse[MemberResp])
def delete_member(id : int,response : Response , db : Annotated[Session , Depends(get_db)]) :
    member_verify = db.query(Member).filter(Member.id==id)
    member_copy = member_verify.first()
    
    if member_copy : 
        member_verify = member_verify.delete(synchronize_session=False)
        
        user_verify = db.query(User).filter(User.id == member_copy.member_id).delete(synchronize_session=False)
        db.commit()
        return StandardResponse(
                                            success=True , 
                                            data = None ,
                                            message = "Member deleted Successfully"
                                        )
        
    response.status_code = status.HTTP_404_NOT_FOUND
    return StandardResponse(
                                        success=False , 
                                        data = None ,
                                        message = "Member Searching is failed",
                                        error=ErrorResponse(
                                            code = "NON EXISTING MEMBER",
                                            message="Member does not exist"
                                        )

                                    )
    

@router.get("/search", response_model=StandardResponse[MemberResp])
def get_member(
    db: Annotated[Session, Depends(get_db)],
    response : Response,
    phone_num: int | None = None,
    full_name: str | None = None,
    status_user : UserStatus | None = None
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
    elif status_user is not None :
        member = (
                    db.query(Member)
                    .filter(
                        Member.user.has(User.status == status_user )
                    )
                    .first()
                )
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return StandardResponse(
                                            success=False , 
                                            data = None ,
                                            message = "Member Searching is failed", 
                                            error = ErrorResponse(
                                                code = "MISSING ARGUMENTS",
                                                message="Provide phone_number or full_name or status",
                                                field="Status,Phone_num,Full_name"
                                            )
                                        )
        

    if not member:
        response.status_code = status.HTTP_404_NOT_FOUND
        return StandardResponse(
                                                    success=False , 
                                                    data = None ,
                                                    message = "Member Searching is failed", 
                                                    error = ErrorResponse(
                                                        code = "NON EXISTING MEMBER",
                                                        message="Member does not exist"
                                                        
                                                    )
                                                )

    return StandardResponse(
                                                success=True , 
                                                data = member ,
                                                message = "Member obtained successfully"
                                            )

@router.patch("/{id}",response_model=StandardResponse[MemberResp])
def modify_member(id : int ,response : Response,data : MemberModify , db : Annotated[Session , Depends(get_db)]) :
    
    member_verify = db.query(Member).filter(Member.id == id).first()
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
        response.status_code = status.HTTP_202_ACCEPTED
        return StandardResponse(
                                                    success=True , 
                                                    data = member_verify ,
                                                    message = "Member Modified Successfully"
                                                )
    response.status_code = status.HTTP_404_NOT_FOUND
    return StandardResponse(
                                                success=False , 
                                                data = None ,
                                                message = "Member Searching is failed", 
                                                error = ErrorResponse(
                                                    code = "NON EXISTING MEMBER",
                                                    message="Member does not exist"
                                                )
                                            )
