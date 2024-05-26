from pydantic import BaseModel, Field


class UserCreate(BaseModel):
  username: str = Field(min_length=1)
  email: str = Field(min_length=1)
  first_name: str = Field(min_length=1)
  last_name: str = Field(min_length=1)
  password: str = Field(min_length=6)
  role: str
  phone_number: str = Field(min_length=9)

  class Config:
      json_schema_extra = {
          'example': {
              'username': '',
              'email': '',
              'first_name': '',
              'last_name': '',
              'password': '',
              'role': '',
              'phone_number': ''
          }
      }

class UserUpdate(BaseModel):
  first_name: str = Field()
  last_name: str = Field()
  phone_number: str = Field()

  class Config:
      json_schema_extra = {
          'example': {
              'first_name': '',
              'last_name': '',
              'phone_number': ''
          }
      }

class UserResponse(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    phone_number: str

class UserChangedPassword(BaseModel):
  current_password: str = Field(min_length=3, max_length=80)
  changed_password: str = Field(min_length=3, max_length=80)

  class Config:
    json_schema_extra = {
      'example': {
        'current_password': '',
        'changed_password': '',
      }
    }
