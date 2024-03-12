# main.py
from fastapi import FastAPI
from app.api.v1.endpoints import todo
from app.db.database import engine
from app.models.models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(todo.router)
