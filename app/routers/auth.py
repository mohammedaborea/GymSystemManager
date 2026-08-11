from fastapi import APIRouter,Depends,HTTPException,Response,status
from app.oauth2 import authenticate_user,create_access_token
from app.schema import Token,UserResp,UserCreate
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.oauth2 import ACCESS_TOKEN_EXPIRE_MINUTES , get_password_hash
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User


router = APIRouter(prefix="/auth",tags=["auth"])


@router.post("/register")
async def create_user(current_user : UserCreate,response : Response,db : Annotated[Session ,Depends(get_db)]) :
    current_user = current_user.model_dump()
    verify_user = db.query(User).filter(User.phone_number == current_user["phone_number"]).first()
    
    if verify_user :
        raise HTTPException(403,"the user is already exist !")
    hashed_password = get_password_hash(current_user["password"])
    new_user = User(full_name = current_user["full_name"],phone_number = current_user["phone_number"],email = current_user["email"] , notes = current_user["notes"] , role_id = 1)
    db.add(new_user)
    db.commit()
    response.status_code = status.HTTP_201_CREATED
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login_for_access_token(form_data : Annotated[OAuth2PasswordRequestForm,Depends()],db : Annotated[Session,Depends(get_db)])->Token :
    user = authenticate_user(db,email=form_data.username , password= form_data.password)
    if user is None :
        raise HTTPException(401,"Invalid email or password")
    token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded_token = create_access_token({
        "sub" : str(user.id), 
    },expiredelta=token_expire)
    return Token(access_token=encoded_token,token_type="Bearer")

