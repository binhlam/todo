from sqlalchemy.orm import Session

from ..models.todo import Todo
from ..schemas.todo import TodoCreate, TodoUpdate


def get_todo_by_id(db: Session, todo_id: int):
  return db.query(Todo).filter(Todo.id == todo_id).first()

def get_todo_by_user_id(db: Session, user_id: int):
    return db.query(Todo).filter(Todo.user_id == user_id).first()

def get_todos(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Todo).offset(skip).limit(limit).all()

def create_todo(db: Session, todo_create: TodoCreate):
    todo = Todo(**todo_create.dict())

    db.add(todo)
    db.commit()
    db.refresh(todo)

    return todo

def update_todo(db: Session, todo: Todo, todo_update: TodoUpdate):
    todo.title = todo_update.title
    todo.description=todo_update.description,
    todo.priority=todo_update.priority,
    todo.complete = todo_update.complete

    db.add(todo)
    db.commit()
    db.refresh(todo)

    return todo

def delete_todo(db: Session, todo_id: int):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        return

    db.delete(todo)
    db.commit()
