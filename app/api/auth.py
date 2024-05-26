from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..config.exceptions import CreateRecordError
from ..database import get_db
from ..schemas.user import UserCreate
from ..services import user as user_service
from ..services.security import auth as auth_service

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(db: db_dependency,
                 payload: UserCreate):
    try:
        user_service.create_user(db=db, user_create=payload)
    except CreateRecordError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Cannot create user'
        )

@router.post("/signin", status_code=status.HTTP_200_OK)
async def sign_in(db: db_dependency,
                  form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = auth_service.authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Failed Authentication')

    try:
        access_token = auth_service.generate_access_token(user.username,
                                            user.id,
                                            user.role,
                                            timedelta(minutes=20))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Signin error'
        )

    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }
