from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...config.exceptions import (CreateRecordError, DeleteRecordError,
                                  PermissionDenied, RecordNotFound,
                                  UpdateRecordError)
from ...database import get_db
from ...models.user import User
from ...schemas.user import (UserChangedPassword, UserCreate, UserResponse,
                             UserUpdate)
from ...services import user as user_service
from ...services.security.auth import get_current_user

router = APIRouter(
  prefix='/v1',
  tags=['user']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[User, Depends(get_current_user)]

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(db: db_dependency,
                   current_user: user_dependency,
                   user_id: int):
  try:
    user = user_service.get_user_by_id(
      db=db,
      current_user=current_user, 
      user_id=user_id
    )
  except RecordNotFound:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail='Record not found'
    )
  except PermissionDenied:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail='Permission Denied.'
    )
  
  return user

@router.put("/users/{user_id}/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(db: db_dependency,
                          current_user: user_dependency,
                          user_id: int,
                          request: UserChangedPassword):
  try:
    user = user_service.change_password(
      db=db, 
      author=current_user,
      user_id=user_id,
      user_changed_password=request
    )
  except UpdateRecordError:
    raise HTTPException(
      status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
      detail='Cannot update password.'
    )
  except PermissionDenied:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail='Permission Denied.'
    )
  
  return user

@router.put("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update(db: db_dependency,
                 current_user: user_dependency,
                 user_id: int,
                 request: UserUpdate):
  try:
    user = user_service.update_user(
      db=db, 
      author=current_user,
      user_id=user_id, 
      user_update=request
    )
  except UpdateRecordError:
    raise HTTPException(
      status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
      detail='Cannot update user.'
    )
  except PermissionDenied:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail='Permission Denied.'
    )

  return user
