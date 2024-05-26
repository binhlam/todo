import logging
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from ...config.exceptions import RecordNotFound
from ...database import get_db
from .. import user as user_service
from ..security.utils import (ALGORITHM, SECRECT_KEY, bcrypt_context,
                              oauth2_bearer)

logger = logging.getLogger(__name__)

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

def authenticate_user(db: Session, username: str, password: str):
    user = user_service.get_user_by_username(db=db, username=username)
    if user is None:
        raise RecordNotFound(record_type='User', record_name='Username', record_val=username)
    
    is_verified = bcrypt_context.verify(password, user.hashed_password)
    if not is_verified:
        return False

    return user

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    def get_user():
        db: Session = next(get_db())
        admin = user_service.get_admin(db=db)
        user = user_service.get_user_by_id(
            db=db, 
            current_user=admin, 
            user_id=extracted_user['id']
        )
        return user

    try:
        extracted_user = jwt.decode(token, SECRECT_KEY, algorithms=[ALGORITHM])
        validate_user(extracted_user)
        user = get_user()
    except JWTError as e:
        logger.error("Error parsing JWT token: ", str(e))
        return

    return user

def validate_user(user: dict):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Unauthorized user')
    
    if user.get('id', -1) < 0:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Unauthorized user_id')
    
    return True
