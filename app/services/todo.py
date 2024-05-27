import logging

from sqlalchemy.orm import Session

from ..models.todo import Todo
from ..repositories import todo as todo_repo
from ..schemas.todo import TodoCreate, TodoUpdate

logger = logging.getLogger(__name__)


from ..config.exceptions import (CreateRecordError, DeleteRecordError,
                                 RecordNotFound, UpdateRecordError)


def get_todos(db: Session):
  return todo_repo.get_todos(db)

def get_todos_by_user_id(db: Session, user_id: int):
  return todo_repo.get_todo_by_user_id(db, user_id)

def get_todo(db: Session, todo_id:int):
  return todo_repo.get_todo_by_id(db, todo_id)

def create_todo(db: Session, todo_create: Todo):
  todo = todo_repo.create_todo(db=db, todo_create=todo_create)
  if todo is None:
    logger.error('Cannot create todo with data: {user_create}}')
    raise CreateRecordError(record_type='Todo')
  
  return todo

def update_todo(db: Session, todo_id: int, todo_update: TodoUpdate):
  todo = todo_repo.get_todo_by_id(db=db, todo_id=todo_id)
  if todo is None:
    raise RecordNotFound(record_type='Todo', record_name='ID', record_val=todo_id)
  
  todo = todo_repo.update_todo(db=db, todo=todo, todo_update=todo_update)
  if todo is None:
    raise UpdateRecordError(record_type='Todo', record_id=todo_id)
  
  return todo

def delete_todo(db: Session, todo_id: int):
  todo = todo_repo.get_todo_by_id(db=db, todo_id=todo_id)
  if todo is None:
    raise RecordNotFound(record_type='Todo', record_name='ID', record_val=todo_id)
  
  try:
    todo = todo_repo.delete_todo(db=db, todo_id=todo_id)
  except Exception:
    raise DeleteRecordError(record_type='Todo', record_id=todo_id)
  
  return
