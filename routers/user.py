from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Path
from ..models import User
from ..database import get_db
from .auth import get_current_user, bcrypt_context
from pydantic import BaseModel, Field

router = APIRouter(
  prefix='/user',
  tags=['user']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class UserResponse(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    phone_number: str

class UserRequest(BaseModel):
  email: str = Field(min_length=1, max_length=80)
  first_name: str = Field(min_length=1, max_length=80)
  last_name: str = Field(min_length=1, max_length=80)
  phone_number: str = Field(min_length=8, max_length=11)

  class Config:
    json_schema_extra = {
      'example': {
        'email': '',
        'first_name': '',
        'last_name': '',
        'phone_number': '',
      }
    }

class ChangePasswordRequest(BaseModel):
  current_password: str = Field(min_length=3, max_length=80)
  changed_password: str = Field(min_length=3, max_length=80)

  class Config:
    json_schema_extra = {
      'example': {
        'current_password': '',
        'changed_password': '',
      }
    }

def validate_user(user_info: dict):
  if not user_info:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Unauthorized user!')

  if user_info.get('id', -1) < 0:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Unauthorized admin!')
  return

def get_user_by_id(user_id: int, db):
  return db.query(User).filter(User.id == user_id).first()

@router.get("/info", response_model=UserResponse)
async def read(db: db_dependency,
               user: user_dependency):
  validate_user(user)

  user = get_user_by_id(user['id'], db)
  return user

@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(db: db_dependency,
                          user: user_dependency,
                          payload: ChangePasswordRequest):
  validate_user(user)

  user = get_user_by_id(user['id'], db)
  is_verified = bcrypt_context.verify(payload.current_password, user.hashed_password)
  if not is_verified:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Current password is invalid!')

  user.hashed_password = bcrypt_context.hash(payload.changed_password)
  db.add(user)
  db.commit()

@router.put("", status_code=status.HTTP_204_NO_CONTENT)
async def update(db: db_dependency,
                          user: user_dependency,
                          payload: UserRequest):
  validate_user(user)

  user = get_user_by_id(user['id'], db)
  user.email = payload.email
  user.first_name = payload.first_name
  user.last_name = payload.last_name
  user.phone_number = payload.phone_number

  db.add(user)
  db.commit()
