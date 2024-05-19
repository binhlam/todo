from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from ..models import Todo
from ..database import get_db
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/todos")
async def read_all(db: db_dependency,
                   user: user_dependency):
  if not user or not user.get('id', -1):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                        detail='Unauthorized user!')
  
  if user.get('role', '') == 'admin':
    return db.query(Todo).all()
  
  return db.query(Todo).filter(Todo.owner_id == user['id']).all()

@router.get("/todos/{todo_id}")
async def read_all(db: db_dependency, todo_id: int):
  todo = db.query(Todo).filter(Todo.id == todo_id).first()
  if not todo:
    raise HTTPException(status_code=404, detail='Record not found.')
  
  return todo

class TodoRequest(BaseModel):
  title: str = Field(min_length=3, max_length=80)
  description: str = Field(min_length=3, max_length=200)
  priority: int = Field(gt=0)
  complete: int

  class Config:
    json_schema_extra = {
      'example': {
        'title': 'A new item',
        'description': 'item desc',
        'priority': 0,
        'complete': 0
      }
    }

@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def create(db: db_dependency,
                 user: user_dependency,
                 todo_request: TodoRequest):
  if not user or not user.get('id', -1):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                        detail='Unauthorized user!')

  todo = Todo(**todo_request.dict(), owner_id=user['id'])
  db.add(todo)
  db.commit()

@router.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update(db: db_dependency,
                 user: user_dependency,
                 todo_id: int,
                 todo_request: TodoRequest):
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                        detail='Unauthorized user!')

  todo = db.query(Todo).filter(Todo.id == todo_id).first()
  if not todo:
    raise HTTPException(status_code=404, detail='Record not found.')

  todo_req = Todo(**todo_request.dict())
  todo.title = todo_req.title
  todo.description = todo_req.description
  todo.priority = todo_req.priority
  todo.complete = todo_req.complete

  db.add(todo)
  db.commit()

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(db: db_dependency,
                 user: user_dependency,
                 todo_id: int):
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                        detail='Unauthorized user!')

  todo = db.query(Todo).filter(Todo.id == todo_id).first()
  if not todo:
    raise HTTPException(status_code=404, detail='Record not found.')

  db.delete(todo)
  db.commit()
