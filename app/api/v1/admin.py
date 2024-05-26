from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...database import get_db
from ...repositories import todo as todo_repo
from ...services.security.auth import get_current_user

router = APIRouter(
  prefix='/admin',
  tags=['admin']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/todos")
async def read_all(db: db_dependency,
                   current_user: user_dependency):
  if current_user.role != 'admin':
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Unauthorized admin!')
  
  return todo_repo.get_todos(db=db)
