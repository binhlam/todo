from fastapi import FastAPI

from .api import auth
from .api.v1 import admin, todo, user
from .config.logging import setup_logging
from .database import Base, engine

setup_logging()

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/healthy")
def check_health():
  return {'status': 'healthy'}


app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(user.router)
app.include_router(admin.router)
