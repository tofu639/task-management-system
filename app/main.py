import time
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# ฟังก์ชันรอให้ PostgreSQL พร้อมใช้งาน
def wait_for_db():
    db_url = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/taskdb")
    engine = create_engine(db_url)
    retries = 5
    while retries > 0:
        try:
            engine.connect()
            print("Database is ready!")
            break
        except OperationalError:
            retries -= 1
            print("Database not ready, waiting...")
            time.sleep(5)
    else:
        raise Exception("Could not connect to the database")

# รอให้ PostgreSQL พร้อมใช้งาน
wait_for_db()

# ส่วนที่เหลือของโค้ด FastAPI
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)

@app.get("/tasks/", response_model=list[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks

@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = crud.update_task(db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.delete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}