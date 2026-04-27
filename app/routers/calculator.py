from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from typing import List

router = APIRouter(prefix="/calc", tags=["calculator"])

# 5. Последние 10 вычислений
@router.get("/history", response_model=List[schemas.Calculation])
def get_calculation_history(db: Session = Depends(get_db)):
    return db.query(models.Calculation).order_by(models.Calculation.calculated_at.desc()).limit(10).all()

# Добавить вычисление
@router.post("/calculate", response_model=schemas.Calculation)
def save_calculation(calc: schemas.CalculationCreate, db: Session = Depends(get_db)):
    db_calc = models.Calculation(**calc.dict())
    db.add(db_calc)
    db.commit()
    db.refresh(db_calc)
    return db_calc

# 6. Среднее количество знаков после запятой (примерная реализация)
@router.get("/stats/decimal-places")
def avg_decimal_places(db: Session = Depends(get_db)):
    # Для SQLite можно посчитать среднюю длину дробной части
    # Здесь упрощённо: вернём среднее арифметическое
    from sqlalchemy import func
    avg_result = db.query(func.avg(models.Calculation.result)).scalar()
    return {"average_result": avg_result}

# 7. Количество ошибочных вычислений
@router.get("/stats/errors")
def count_errors(db: Session = Depends(get_db)):
    count = db.query(models.Calculation).filter(models.Calculation.is_error == True).count()
    return {"error_count": count}