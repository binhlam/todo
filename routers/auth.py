from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field
from ..models import User
from passlib.context import CryptContext
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime


router = APIRouter(
  prefix='/auth',
  tags=['auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/signin')

SECRECT_KEY = '4e5443c8495db2010f69d7828b61f2c71d5f2030c740217143f841f352550f0a'
ALGORITHM = 'HS256' 

db_dependency = Annotated[Session, Depends(get_db)]


class UserRequest(BaseModel):
  username: str = Field(min_length=1)
  email: str = Field(min_length=1)
  first_name: str = Field(min_length=1)
  last_name: str = Field(min_length=1)
  password: str = Field(min_length=6)
  role: str
  phone_number: str = Field(min_length=9)

  class Config:
    json_schema_extra = {
      'example': {
        'username': '',
        'email': '',
        'first_name': '',
        'last_name': '',
        'password': '',
        'role': '',
        'phone_number': ''
      }
    }

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create(db: db_dependency,
                 payload: UserRequest):
  user = User(
    username=payload.username,
    email=payload.email,
    first_name=payload.first_name,
    last_name=payload.last_name,
    hashed_password=bcrypt_context.hash(payload.password),
    role=payload.role,
    phone_number=payload.phone_number,
    is_active=True
  )

  db.add(user)
  db.commit()


def generate_access_token(username: str, 
                          user_id: int,
                          role: str,
                          expires_delta: timedelta):
  data = {
    'sub': username,
    'id': user_id,
    'role': role,
    'exp': datetime.utcnow() + expires_delta
  }

  return jwt.encode(data, SECRECT_KEY, algorithm=ALGORITHM)

def authenticate_user(username: str, password: str, db):
  user = db.query(User).filter(User.username == username).first()
  if not user:
    return False
  
  is_verified = bcrypt_context.verify(password, user.hashed_password)
  if not is_verified:
    return False
  
  return user

@router.post("/signin", status_code=status.HTTP_200_OK)
async def sign_in(db: db_dependency,
                  form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
  user = authenticate_user(form_data.username, form_data.password, db)
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Failed Authentication')
  
  access_token = generate_access_token(user.username,
                                       user.id,
                                       user.role,
                                       timedelta(minutes=20))
  return {
    'access_token': access_token,
    'token_type': 'bearer'
  }

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
  try:
    user = jwt.decode(token, SECRECT_KEY, algorithms=[ALGORITHM])
    username = user.get('sub', '')
    user_id = user.get('id', -1)
    if not username or not user_id:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized user')
    
    return user
  except JWTError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized user')

