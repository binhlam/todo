from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
  title: str = Field(min_length=3, max_length=80)
  description: str = Field(min_length=3, max_length=200)
  priority: int = Field(gt=0)
  complete: bool

  class Config:
    json_schema_extra = {
      'example': {
        'title': 'A new item',
        'description': 'item desc',
        'priority': 1,
        'complete': 0
      }
    }
  
class TodoUpdate(BaseModel):
  title: str = Field(min_length=3, max_length=80)
  description: str = Field(min_length=3, max_length=200)
  priority: int = Field(gt=0)
  complete: bool

  class Config:
    json_schema_extra = {
      'example': {
        'title': 'An updated item',
        'description': 'item desc',
        'priority': 1,
        'complete': 0
      }
    }
