from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.database import get_db
from app import models, schemas
from typing import List, Optional
import datetime

router = APIRouter(prefix="/todo", tags=["todo"])

# 3. Незавершённые задачи, сортировка по приоритету DESC, created_at DESC
@router.get("/tasks", response_model=List[schemas.TodoTask])
def get_tasks(completed: Optional[bool] = None, db: Session = Depends(get_db)):
    query = db.query(models.TodoTask)
    if completed is not None:
        query = query.filter(models.TodoTask.is_completed == completed)
    return query.order_by(models.TodoTask.priority.desc(), models.TodoTask.created_at.desc()).all()

# Создание задачи
@router.post("/tasks", response_model=schemas.TodoTask)
def create_task(task: schemas.TodoTaskCreate, db: Session = Depends(get_db)):
    db_task = models.TodoTask(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# 4. Отметить задачу завершённой
@router.put("/tasks/{task_id}/complete")
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.TodoTask).filter(models.TodoTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.is_completed = True
    task.completed_at = datetime.utcnow()
    db.commit()
    return {"status": "completed"}

# Обновление задачи (toggle)
@router.put("/tasks/{task_id}", response_model=schemas.TodoTask)
def update_task(task_id: int, task_update: schemas.TodoTaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.TodoTask).filter(models.TodoTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    if update_data.get("is_completed") is True and not task.completed_at:
        task.completed_at = datetime.utcnow()
    elif update_data.get("is_completed") is False:
        task.completed_at = None
    db.commit()
    db.refresh(task)
    return task

# Удаление задачи
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.TodoTask).filter(models.TodoTask.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
    return {"ok": True}

# 5. Количество задач по категории и статусу
@router.get("/tasks/stats")
def get_task_stats(db: Session = Depends(get_db)):
    stats = db.query(
        models.TodoTask.category,
        models.TodoTask.is_completed,
        func.count(models.TodoTask.id).label("count")
    ).group_by(models.TodoTask.category, models.TodoTask.is_completed).all()
    result = {}
    for cat, comp, cnt in stats:
        cat = cat or "Без категории"
        if cat not in result:
            result[cat] = {"completed": 0, "active": 0}
        if comp:
            result[cat]["completed"] = cnt
        else:
            result[cat]["active"] = cnt
    return result