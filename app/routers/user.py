from app.database import get_db
from app.models import User,Member
from fastapi import APIRouter,Depends,HTTPException,Response,status
from sqlalchemy.orm import Session
from app.schema import UserResp,UserCreate,UserBase , RoleUpdate,passwordChange
from typing import List,Annotated
from app.oauth2 import get_password_hash , get_current_user , admin_required,verify_password

router = APIRouter(prefix="/member",tags=["members"])

@router.get("/")
def get_members(db : Annotated[Session , Depends(get_db)]) :
    members = db.query(Member).all()
    return members
















