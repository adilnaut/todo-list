from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....db.database import SessionLocal
from ....models.models import TodoList, TodoItem
from ....schemas.schemas import ( TodoListCreate, TodoListDisplay, TodoItemDisplay, TodoItemCreate,
    TodoListNameUpdate, TodoItemDeadlineUpdate)

router = APIRouter()

def get_db():
    ''' Utility function to wrap db session object and close on completion.'''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/todo/list/", response_model=TodoListDisplay)
def create_list(todo_list: TodoListCreate, db: Session = Depends(get_db)):
    db_todo_list = TodoList(name=todo_list.name)
    db.add(db_todo_list)
    # For each item in the todo list, create and add a TodoItem instance
    for item_data in todo_list.items:
        db_todo_item = TodoItem(**item_data.dict(), list=db_todo_list) # Linking the item to the list
        db.add(db_todo_item)
    db.commit()
    db.refresh(db_todo_list)
    # Refresh each item to ensure they are loaded
    for item in db_todo_list.items:
        db.refresh(item)
    return db_todo_list

@router.get("/todo/list/", response_model=List[TodoListDisplay])
def read_lists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todo_lists = db.query(TodoList).offset(skip).limit(limit).all()
    return todo_lists

@router.get("/todo/list/{list_id}/", response_model=List[TodoItemDisplay])
def read_todo_list(list_id:int, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    ''' Return todo list view by list_id. 
    '''
    todo_list = db.query(TodoList).filter(TodoList.id == list_id).first()
    if not todo_list:
        raise HTTPException(status_code=404, detail="Todo list not found")
    todo_items = db.query(TodoItem).filter(TodoItem.list_id == list_id).offset(skip).limit(limit).all()
    return todo_items

@router.post("/todo/list/{list_id}/item/", response_model=TodoItemDisplay)
def add_item_to_list(list_id: int, item: TodoItemCreate, db: Session = Depends(get_db)):
    todo_list = db.query(TodoList).filter(TodoList.id == list_id).first()
    if todo_list is None:
        raise HTTPException(status_code=404, detail="Todo list not found")
    db_todo_item = TodoItem(**item.dict(), list_id=todo_list.id)
    db.add(db_todo_item)
    db.commit()
    db.refresh(db_todo_item)
    return db_todo_item

@router.patch("/todo/item/{item_id}/complete/", response_model=TodoItemDisplay)
def mark_item_as_completed(item_id: int, db: Session = Depends(get_db)):
    todo_item = db.query(TodoItem).filter(TodoItem.id == item_id).first()
    if todo_item is None:
        raise HTTPException(status_code=404, detail="Todo item not found")
    todo_item.completed = True
    db.commit()
    db.refresh(todo_item)
    return todo_item

@router.patch("/todo/item/{item_id}/deadline/", response_model=TodoItemDisplay)
def attach_deadline_to_item(item_id: int, dl_item: TodoItemDeadlineUpdate, db: Session = Depends(get_db)):
    todo_item = db.query(TodoItem).filter(TodoItem.id == item_id).first()
    if todo_item is None:
        raise HTTPException(status_code=404, detail="Todo item not found")
    todo_item.deadline = dl_item.deadline
    db.commit()
    db.refresh(todo_item)
    return todo_item


@router.delete("/todo/item/{item_id}/", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    todo_item = db.query(TodoItem).filter(TodoItem.id == item_id).first()
    if todo_item is None:
        raise HTTPException(status_code=404, detail="Todo item not found")
    db.delete(todo_item)
    db.commit()
    return {"detail": "Todo item deleted"}

@router.delete("/todo/list/{list_id}/", status_code=204)
def delete_list(list_id: int, db: Session = Depends(get_db)):
    todo_list = db.query(TodoList).filter(TodoList.id == list_id).first()
    if todo_list is None:
        raise HTTPException(status_code=404, detail="Todo list not found")
    db.delete(todo_list)
    db.commit()
    return {"detail": "Todo list deleted"}

@router.patch("/todo/list/{list_id}/name/", response_model=TodoListDisplay)
def change_list_name(list_id: int, name_update: TodoListNameUpdate, db: Session = Depends(get_db)):
    todo_list = db.query(TodoList).filter(TodoList.id == list_id).first()
    if todo_list is None:
        raise HTTPException(status_code=404, detail="Todo list not found")
    todo_list.name = name_update.name
    db.commit()
    db.refresh(todo_list)
    return todo_list
