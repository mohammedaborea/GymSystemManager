from typing import Annotated
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Admin
from fastapi import Depends,HTTPException,FastAPI,APIRouter
from pwdlib import PasswordHash
from app.schemas.authOTD import Token,TokenData
from datetime import timedelta,timezone,datetime
from jwt.exceptions import InvalidTokenError
import jwt
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from pydantic import EmailStr
from app.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES




oauth2_scheme =OAuth2PasswordBearer(tokenUrl="login") 

password_hash = PasswordHash.recommended()

def verify_password(plain_password,hash_password) :
    return password_hash.verify(plain_password,hash_password)

def get_password_hash(plain_password) :
    return password_hash.hash(plain_password)

def create_access_token(data : dict , expiredelta : timedelta | None = None ) :
    to_encode = data.copy()
    if expiredelta :
        expire = datetime.now(timezone.utc) + expiredelta
    else :
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def get_user(db : Session , id : int) :
    user_verify = db.query(Admin).filter(Admin.id == id).first()
    if not user_verify :
        raise HTTPException(404,"user does not exist")
    return user_verify
    

def get_current_user(db :Annotated[Session,Depends(get_db)],token : Annotated[str,Depends(oauth2_scheme)]) :
    
    credentials_exception = HTTPException(401,"could not validate credentials")
    try :
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        user_id = payload.get("sub")
        if user_id is None :
            
            raise credentials_exception
        token_data = TokenData(id=user_id)
    except InvalidTokenError as e:
        
        raise credentials_exception
    current_user = get_user(db,token_data.id)
    if current_user is None :
        
        raise credentials_exception
    
    return current_user

def authenticate_user(db :Session , 
                      email:EmailStr,
                      password : str) :
    user_verify = db.query(Admin).filter(Admin.email == email).first()
    if not user_verify :
        raise HTTPException(404,"email does not exist")
    if not verify_password(password,user_verify.password) :
        raise HTTPException(401,"check your password")
    return user_verify











