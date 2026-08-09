from app.database import get_db
from app.models import User
from fastapi import APIRouter,Depends,HTTPException,Response,status
from sqlalchemy.orm import Session
from app.schema import UserResp,UserCreate,UserBase , RoleUpdate,passwordChange
from typing import List,Annotated
from app.oauth2 import get_password_hash , get_current_user , admin_required,verify_password

router = APIRouter(prefix="/user",tags=["users"])




# admin
@router.get("/",response_model=List[UserResp])
async def get_users(db : Annotated[Session,Depends(get_db)],current_user = Depends(get_current_user),admin = Depends(admin_required) ) :
    users = db.query(User).all()
    return users



@router.get("/me",response_model=UserBase)
async def get_me(db : Annotated[Session,Depends(get_db)],current_user = Depends(get_current_user)) :
    return current_user

@router.patch("/me")
async def get_me(user_data : UserResp,db : Annotated[Session,Depends(get_db)],current_user = Depends(get_current_user)) :
    user = db.query(User).filter(User.id == current_user.id).first()
    user.email = user_data.email
    user.full_name = user_data.full_name
    db.commit()
    db.refresh(user)
    return user

@router.patch("/me/password")
async def get_me(password : passwordChange,db : Annotated[Session,Depends(get_db)],current_user = Depends(get_current_user)) :
    user = db.query(User).filter(User.id == current_user.id).first()
    if not verify_password(password.current_password,user.password) :
        raise HTTPException(403,"password is wrong")
    user.password = get_password_hash(password.new_password)
    db.commit()
    db.refresh(user)
    return user


# admin
@router.get("/{id}",response_model=UserResp)
async def get_user(id : int,db : Annotated[Session,Depends(get_db)],current_user = Depends(get_current_user),admin = Depends(admin_required)) :
    user = db.query(User).filter(User.id == id).first()
    if not user : 
        raise HTTPException(404,f"user with id {id} does not exist")
    return user

# admin
@router.patch("/{id}/role")
async def change_role(id : int ,
                      role :RoleUpdate,
                      db : Annotated[Session,Depends(get_db)],
                      current_user = Depends(get_current_user),
                      admin = Depends(admin_required) ) :
    user = db.query(User).filter(User.id == id).first()
    if not user : 
        raise HTTPException(404,f"user with id {id} does not exist")
    if user.role == role.role.value :
        raise HTTPException(403,"user actually has that role !")
    user.role = role.role.value
    db.commit()
    db.refresh(user)
    return user









