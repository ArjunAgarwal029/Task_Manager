from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import engine,sessionLocal
import models
# from pydantic import BaseModel
from typing import Optional
# from datetime import datetime
import schema
app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create Task
@app.post("/tasks/", status_code=status.HTTP_201_CREATED)
def create_task(request: schema.TaskSchema, db: Session = Depends(get_db)):
    new_task = models.Task(
        title=request.title,
        description=request.description,
        due_date=request.due_date,
        is_complete=request.is_complete,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# Get All Tasks
@app.get("/tasks/",status_code=status.HTTP_200_OK)
def list_tasks(is_complete: Optional[bool] = None, db: Session = Depends(get_db)):
    query = db.query(models.Task)
    if is_complete is not None:
        query = query.filter(models.Task.is_complete == is_complete)
    tasks = query.all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    return tasks

# Get Task by ID
@app.get("/tasks/{task_id}/",status_code=status.HTTP_200_OK )
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    return task

# Update Task
@app.put("/tasks/{task_id}/", status_code=status.HTTP_202_ACCEPTED)
def update_task(task_id: int, request: schema.TaskSchema, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    task.title = request.title or task.title
    task.description = request.description or task.description
    task.due_date = request.due_date or task.due_date
    task.is_complete = request.is_complete or task.is_complete
    db.commit()
    db.refresh(task)
    return task

# Delete Task
@app.delete("/tasks/{task_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted successfully"}
