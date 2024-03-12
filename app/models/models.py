# /app/models/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.database import Base

class TodoList(Base):
    __tablename__ = "todo_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    items = relationship("TodoItem", back_populates="list")

class TodoItem(Base):
    __tablename__ = "todo_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    deadline = Column(DateTime, nullable=True)
    completed = Column(Boolean, default=False)
    list_id = Column(Integer, ForeignKey("todo_lists.id"))

    list = relationship("TodoList", back_populates="items")
