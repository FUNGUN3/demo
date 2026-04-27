# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.database import get_db
from app import models, schemas
from app.auth import hash_password, verify_password
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

# Вспомогательная функция для получения возраста
def is_adult(birth_date: datetime) -> bool:
    """Проверяет, старше ли пользователь 18 лет"""
    if not birth_date:
        return False
    today = datetime.utcnow()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age >= 18

# ========== ЭНДПОИНТЫ ==========

# 3. Проверка существования email
@router.get("/check-email")
def check_email(email: str, db: Session = Depends(get_db)):
    """
    Проверяет, зарегистрирован ли email.
    Возвращает: {"exists": true/false}
    """
    user = db.query(models.User).filter(models.User.email == email).first()
    return {"exists": user is not None}

# Регистрация нового пользователя (с реальным хэшированием)
@router.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Регистрирует нового пользователя с хэшированием пароля через bcrypt.
    """
    # Проверка уникальности email
    existing_user = db.query(models.User).filter(
        models.User.email == user_data.email
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже зарегистрирован"
        )
    
    # Хэшируем пароль через bcrypt
    hashed_pw = hash_password(user_data.password)
    
    # Создаём нового пользователя
    db_user = models.User(
        email=user_data.email,
        password_hash=hashed_pw,  # Сохраняем реальный хэш
        full_name=user_data.full_name,
        birth_date=user_data.birth_date,
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# Аутентификация пользователя (логин)
@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    """
    Проверяет email и пароль пользователя.
    При успехе обновляет last_login.
    """
    # Ищем пользователя по email
    user = db.query(models.User).filter(models.User.email == email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )
    
    # Проверяем пароль через bcrypt
    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )
    
    # Обновляем last_login
    user.last_login = datetime.utcnow()
    db.commit()
    
    return {
        "message": "Вход выполнен успешно",
        "user_id": user.id,
        "email": user.email,
        "last_login": user.last_login
    }

# 4. Получение пользователей старше 18 лет
@router.get("/adults", response_model=List[schemas.User])
def get_adult_users(db: Session = Depends(get_db)):
    """
    Возвращает всех пользователей старше 18 лет.
    Использует SQL-запрос: birth_date < CURRENT_DATE - INTERVAL '18 years'
    """
    # Вычисляем дату 18 лет назад
    eighteen_years_ago = datetime.utcnow() - timedelta(days=365.25 * 18)
    
    users = db.query(models.User).filter(
        models.User.birth_date.isnot(None),  # Исключаем пользователей без даты рождения
        models.User.birth_date < eighteen_years_ago
    ).all()
    
    return users

# 5. Обновление last_login для конкретного пользователя
@router.post("/{user_id}/login")
def update_last_login(user_id: int, db: Session = Depends(get_db)):
    """
    Обновляет last_login для пользователя на текущий момент.
    Соответствует запросу: UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = 2
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    # Обновляем время последнего входа
    user.last_login = datetime.utcnow()
    db.commit()
    db.refresh(user)
    
    return {
        "user_id": user.id,
        "email": user.email,
        "last_login": user.last_login
    }

# Получение всех пользователей (дополнительный эндпоинт для тестирования)
@router.get("/", response_model=List[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    """
    Возвращает всех пользователей.
    """
    users = db.query(models.User).all()
    return users

# Получение пользователя по ID
@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Возвращает пользователя по ID.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    return user