from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Numeric, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

# ---------- Задание 1: Блог ----------
class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(150), unique=True, nullable=False, index=True)
    content = Column(Text, nullable=False)
    published_at = Column(DateTime, server_default=func.now())
    is_active = Column(Boolean, default=True)
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    theme_preference = Column(String(20), default="light")

# ---------- Задание 2: Пользователи ----------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    birth_date = Column(DateTime)  # храним как дату
    registered_at = Column(DateTime, server_default=func.now())
    is_confirmed = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)

# ---------- Задание 3: Галерея ----------
class GalleryImage(Base):
    __tablename__ = "gallery_images"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    thumb_url = Column(String(500), nullable=False)
    full_url = Column(String(500), nullable=False)
    alt_text = Column(String(200))
    description = Column(Text)
    upload_date = Column(DateTime, server_default=func.now())
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    category = Column(String(50))

# ---------- Задание 4: Задачи ----------
class TodoTask(Base):
    __tablename__ = "todo_tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)  # Можно привязать к пользователю позже
    task_text = Column(String(500), nullable=False)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)
    priority = Column(Integer, default=0)  # 0 низкий, 1 средний, 2 высокий
    category = Column(String(50))

# ---------- Задание 5: Калькулятор ----------
class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    expression = Column(Text, nullable=False)
    result = Column(Numeric, nullable=False)
    calculated_at = Column(DateTime, server_default=func.now())
    is_error = Column(Boolean, default=False)

class CalculatorSettings(Base):
    __tablename__ = "calculator_settings"

    user_id = Column(Integer, primary_key=True)
    decimal_places = Column(Integer, default=2)
    theme = Column(String(20), default="light")