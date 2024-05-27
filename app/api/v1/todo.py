from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...config.exceptions import (CreateRecordError, DeleteRecordError,
                                  RecordNotFound, UpdateRecordError)
from ...database import get_db
from ...models.todo import Todo
from ...models.user import User
from ...schemas.todo import TodoCreate, TodoUpdate
from ...services import todo as todo_service
from ...services.security.auth import get_current_user

router = APIRouter(
  prefix='/v1',
  tags=['todo']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[User, Depends(get_current_user)]

@router.get("/todos")
async def get_todos(db: db_dependency,
                   current_user: user_dependency):
  if current_user.role == 'admin':
    return todo_service.get_todos(db)

  return todo_service.get_todos_by_user_id(db, current_user.id)

@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: db_dependency,
                         current_user: user_dependency, 
                         todo_id: int):
  todo = todo_service.get_todo(db=db, todo_id=todo_id)
  if not todo:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, 
      detail='Record not found.'
    )
  
  return todo

@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def create(db: db_dependency,
                 current_user: user_dependency,
                 request: TodoCreate):
  
  try:
    todo = Todo(**request.dict(), owner_id=current_user.id)
    todo_service.create_todo(db=db, todo_create=todo)
  except CreateRecordError:
    raise HTTPException(
      status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
      detail='Cannot create record.'
    )

@router.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update(db: db_dependency,
                 current_user: user_dependency,
                 todo_id: int,
                 request: TodoUpdate):
  try:
    todo_service.update_todo(db=db, todo_id=todo_id, todo_update=request)
  except RecordNotFound:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, 
      detail='Record not found.'
    )
  except UpdateRecordError:
    raise HTTPException(
      status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
      detail='Cannot update record.'
    )


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(db: db_dependency,
                 current_user: user_dependency,
                 todo_id: int):
  try:
    todo_service.delete_todo(db=db, todo_id=todo_id)
  except RecordNotFound:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, 
      detail='Record not found.'
    )
  except DeleteRecordError:
    raise HTTPException(
      status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
      detail='Cannot delete record.'
    )
