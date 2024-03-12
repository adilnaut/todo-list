from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TodoItemBase(BaseModel):
    title: str
    deadline: Optional[datetime] = None

class TodoItemCreate(TodoItemBase):
    pass

# This is for response view
class TodoItemDisplay(TodoItemBase):
    id: int
    list_id: int
    completed: bool

    # for proper de-serialization
    class Config:
        from_attributes = True

class TodoListBase(BaseModel):
    name: str

class TodoListCreate(TodoListBase):
    items: List[TodoItemCreate] = []  # Allow for an empty list of items

class TodoListDisplay(TodoListBase):
    id: int
    items: List[TodoItemDisplay] = []


    # for proper de-serialization
    class Config:
        from_attributes = True

class TodoListNameUpdate(BaseModel):
    name: str

class TodoItemDeadlineUpdate(BaseModel):
    deadline: datetime
