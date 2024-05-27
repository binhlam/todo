from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from ..database import Base


class Todo(Base):
  __tablename__ = 'todos'

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String)
  description = Column(String)
  priority = Column(Integer)
  complete = Column(Integer, default=False)
  owner_id = Column(Integer, ForeignKey("users.id"))
