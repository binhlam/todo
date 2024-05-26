from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..api.auth import bcrypt_context
from ..models.models import User

DATABASE_URL = 'postgresql://localhost:5432/todo_test'

engine = create_engine(DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def override_get_db():
  db = TestSessionLocal()
  try:
    yield db
  finally:
    db.close()
  
def override_get_current_user():
  return {
    'sub': 'binh.lam',
    'id': 1,
    'role': 'admin'
  }

def init_user():
  user = User(
    email='user01@gmail.com',
    username='user01',
    first_name='User',
    last_name='01',
    hashed_password=bcrypt_context.hash('user1234'),
    role='',
    phone_number='0911234567'
  )
  db = TestSessionLocal()
  db.add(user)
  db.commit()
  
  return user


def init_admin():
  admin = User(
    email='admin01@gmail.com',
    username='admin01',
    first_name='Admin',
    last_name='01',
    hashed_password=bcrypt_context.hash('admin1234'),
    role='admin',
    phone_number='0911234567'
  )
  db = TestSessionLocal()
  db.add(user)
  db.commit()

  return admin