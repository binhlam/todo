import logging

from sqlalchemy.orm import Session

from ..config.exceptions import (CreateRecordError, DeleteRecordError, Error,
                                 PermissionDenied, RecordNotFound,
                                 UpdateRecordError)
from ..models.user import User
from ..repositories import user as user_repo
from ..schemas.user import UserChangedPassword, UserCreate, UserUpdate
from .security.utils import bcrypt_context

logger = logging.getLogger(__name__)


def get_users(db: Session, current_user: User):
  if current_user.role != 'admin':
    raise Error("No permission.")

  return user_repo.get_users(db)

def get_user_by_username(db: Session, username: str):
  user = user_repo.get_user_by_username(db=db, username=username)
  if user is None:
    raise RecordNotFound(record_type='User', record_name='Username', record_val=username)

  return user

def get_admin(db: Session):
  return user_repo.get_user_by_id(db=db, user_id=1)

def get_user_by_id(db: Session, current_user: User, user_id: int):
  if current_user.role != 'admin':
    if current_user.id != user_id:
      raise PermissionDenied

  user = user_repo.get_user_by_id(db=db, user_id=user_id)
  if user is None:
    logger.error('Cannot find user with ID: {user_id}')
    raise RecordNotFound(record_type='User', record_name='ID', record_val=user_id)

  return user

def create_user(db: Session, author: User, user_create: UserCreate):
  if author.role != 'admin':
    raise PermissionDenied

  user_create.password = bcrypt_context.hash(user_create.password)
  user = user_repo.create_user(db=db, user=user_create)
  if user is None:
    logger.error('Cannot create user with data: {user_create}}')
    raise CreateRecordError(record_type='User')
  
  return user 

def update_user(db: Session, author: User, user_id: int, user_update: UserUpdate):
  if author.role != 'admin':
    if author.id != user_id:
      raise PermissionDenied

  user = user_repo.get_user_by_id(db=db, user_id=user_id)
  if user is None:
    raise RecordNotFound(
      record_name='User',
      record_type='ID',
      record_val=user_id
    )

  user = user_repo.update_user(db=db, user=user, user_update=user_update)
  if user is None:
    logger.error('Cannot update user.')
    raise UpdateRecordError(
      record_type='User',
      record_id=user.id
    )
  
  return user

def change_password(db: Session, author: User, user_id: int, user_changed_password: UserChangedPassword):
  if author.role != 'admin':
    if author.id != user_id:
      raise PermissionDenied

  user = user_repo.get_user_by_id(db=db, user_id=user_id)
  if user is None:
    logger.error('Cannot find user with ID: {user_id}')
    raise RecordNotFound(
      record_type='User',
      record_name='ID', 
      record_val=user_id
    )
  
  is_verified = bcrypt_context.verify(user_changed_password.current_password, user.hashed_password)
  if not is_verified:
    raise Error('Current password is invalid.')
  
  updated_password = bcrypt_context.hash(user_changed_password.changed_password)
  user = user_repo.change_password(db=db, user=user, updated_password=updated_password)
  if user is None:
    raise UpdateRecordError(
      record_type='User',
      record_id=user.id
    )
  
  return user
