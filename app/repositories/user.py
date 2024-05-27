from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate


def get_user_by_id(db: Session, user_id: int):
  return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 20):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def update_user(db: Session, user: User, user_update: UserUpdate):
    user.first_name=user_update.first_name or user.first_name,
    user.last_name=user_update.last_name or user.last_name,
    user.phone_number=user_update.phone_number or user.phone_number,
    db.commit()
    db.refresh(user)

    return user

def delete_user(db: Session, user_delete: User):
    db.delete(user_delete)
    db.commit()

    return user_delete

def change_password(db: Session, user: User, updated_password: str):
    user.hashed_password = updated_password
    db.commit()
    db.refresh(user)

    return user
