from sqlalchemy.orm import Session
from app import models, crud
from app.database import SessionLocal

def test_create_task():
    db = SessionLocal()
    task_data = {"title": "Test Task", "description": "This is a test task"}
    task = crud.create_task(db, task_data)
    assert task.title == "Test Task"
    assert task.description == "This is a test task"
    db.close()