from app.database import get_db
from app.models import User,Member,Membership
from fastapi import APIRouter,Depends,HTTPException,Response,status,Query

from sqlalchemy.orm import Session,selectinload
from app.schemas.membership import MembershipCreate,MembershipModify
from app.schemas.common import StandardResponse,ErrorResponse
from typing import List,Annotated
from collections import defaultdict
from datetime import date,timedelta
from app.oauth2 import get_current_user
router = APIRouter(prefix="/membership" , tags=["memberships"],dependencies=[Depends(get_current_user)])

@router.post("/" , response_model=StandardResponse[MembershipCreate])
def add_membership(response : Response,db : Annotated[Session , Depends(get_db)] , membership : MembershipCreate) :
    membership_verify = db.query(Membership).filter(Membership.name == membership.name).first()
    if not membership_verify :
        new_mem = Membership(name = membership.name)
        db.add(new_mem)
        db.commit()
        db.refresh(new_mem)
        return StandardResponse(
            success=True , 
            data = new_mem ,
            message = "Membership Created Successfully"
        )
    response.status_code = status.HTTP_400_BAD_REQUEST
    return StandardResponse(
        success=False ,
        data = None ,
        message = "Membership Creation is Failed" ,
        error = ErrorResponse(
            code = "EXISTING MEMBERSHIP",
            message="Membership Already exists"
        )
    )

@router.get("/",response_model=StandardResponse[List[MembershipCreate]])
def get_membership(db : Annotated[Session , Depends(get_db)],limit : int = 10 , skip : int = 0 ) :
   
    memberships = db.query(Membership).limit(limit).offset(skip).all()
    
    return StandardResponse(
                success=True , 
                data = memberships ,
                message = "Membership Obtained Successfully"
            )


@router.delete("/{id}")
def delete_membership(id : int,response :Response ,db : Annotated[Session , Depends(get_db)]) :
    membership_verify = db.query(Membership).filter(Membership.id == id)
    if membership_verify.first() :
        membership_verify = membership_verify.delete(synchronize_session=False)
        db.commit()
        
        return StandardResponse(
                    success=True , 
                    data = None ,
                    message = "Membership Deleted Successfully"
                )
    response.status_code = status.HTTP_404_NOT_FOUND
    return StandardResponse(
        success=False,
        data=None,
        message = "Membership deleting is failed",
        error = ErrorResponse(
            code = "NON EXISTING MEMBERSHIP",
            message="Membership does not exist"
        )
    )

@router.patch("/{id}",response_model=StandardResponse[MembershipCreate])
def modify_membership(id : int ,response : Response,db : Annotated[Session , Depends(get_db)] , data : MembershipModify) :
    membership_verify = db.query(Membership).filter(Membership.id == id).first()
    if membership_verify:
        membership = data.model_dump(exclude_unset=True)
        for field , value in membership.items() :
            setattr(membership_verify , field , value)
        db.commit()
        db.refresh(membership_verify)
        response.status_code=status.HTTP_202_ACCEPTED
        return StandardResponse(
                        success=True , 
                        data = membership_verify ,
                        message = "Membership Modified Successfully"
                    )
    response.status_code=status.HTTP_404_NOT_FOUND
    return StandardResponse(
            success=False,
            data=None,
            message = "Membership Updating is failed",
            error = ErrorResponse(
                code = "NON EXISTING MEMBERSHIP",
                message="Membership does not exist"
            )
        )


@router.get("/search",response_model=StandardResponse[MembershipCreate])
def get_memb(response : Response,db : Annotated[Session , Depends(get_db)] , pseudo : str) :
    membership_verify = db.query(Membership).filter(Membership.name.contains(pseudo)).first()
    if membership_verify : 
        return StandardResponse(
                                success=True , 
                                data = membership_verify ,
                                message = "Membership Obtained Successfully"
                            )
    response.status_code=status.HTTP_404_NOT_FOUND
    return StandardResponse(
                success=False,
                data=None,
                message = "Membership Obtaining is failed",
                error = ErrorResponse(
                    code = "NON EXISTING MEMBERSHIP",
                    message="Membership does not exist"
                )
            )
    



    


