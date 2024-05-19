from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from ..models import Todo
from ..database import get_db
from .auth import get_current_user

router = APIRouter(
  prefix='/admin',
  tags=['admin']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/todos")
async def read_all(db: db_dependency,
                   user: user_dependency):
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Unauthorized user!')

  if user.get('role', '') != 'admin':
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Unauthorized admin!')
  
  return db.query(Todo).all()
