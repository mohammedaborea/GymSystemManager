from fastapi import APIRouter,Depends,HTTPException,Response,status
from app.oauth2 import authenticate_user,create_access_token
from app.schemas.authOTD import Token,TokenData
from app.schemas.authOTD import AdminCreate,AdminResponse
from app.schemas.common import StandardResponse,ErrorResponse
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.oauth2 import ACCESS_TOKEN_EXPIRE_MINUTES , get_password_hash
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Admin


router = APIRouter(prefix="/auth",tags=["auth"])


@router.post("/register",response_model=StandardResponse[AdminResponse])
async def create_user(current_user : AdminCreate,response : Response,db : Annotated[Session ,Depends(get_db)]) :
    current_user = current_user.model_dump()
    verify_user = db.query(Admin).filter(Admin.email == current_user["email"]).first()
    
    if verify_user :
        response.status_code = status.HTTP_404_NOT_FOUND
        return StandardResponse(success=False,data=None,message="User Registration is failed",error=ErrorResponse(code="EXISTING_EMAIL",
                                                                                                                  message="Email Linked with another account",
                                                                                                                  field = "email"))
    hashed_password = get_password_hash(current_user["password"])
    new_admin = Admin(email = current_user["email"] , password = hashed_password)
    db.add(new_admin)
    db.commit()
    response.status_code = status.HTTP_201_CREATED
    db.refresh(new_admin)
    return StandardResponse(success=True,data=new_admin,message="User Registred Successfully")


@router.post("/login")
def login_for_access_token(form_data : Annotated[OAuth2PasswordRequestForm,Depends()],db : Annotated[Session,Depends(get_db)])->Token :
    user = authenticate_user(db,email=form_data.username , password= form_data.password)
    if user is None :
        return StandardResponse(success=False,data=None,message="User Authentication is failed",error=ErrorResponse(code="INVALID_CREDENTIALS",
                                                                                                                          message="Invalid Email or Password",
                                                                                                                          field = "Email,Password"))
    token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded_token = create_access_token({
        "sub" : str(user.id), 
    },expiredelta=token_expire)
    return Token(access_token=encoded_token,token_type="Bearer")
