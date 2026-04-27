from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional
# ----- Blog -----
class BlogPostBase(BaseModel):
    title: str
    slug: str
    content: str
    theme_preference: str = "light"

class BlogPostCreate(BlogPostBase):
    pass

class BlogPost(BlogPostBase):
    id: int
    published_at: datetime
    is_active: bool
    views_count: int
    likes_count: int

    class Config:
        from_attributes = True

# ----- User -----
class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    birth_date: Optional[datetime] = None

class UserCreate(UserBase):
    password: str  # на фронте передаём пароль, в БД сохраняем хэш (в примере просто как есть)

class User(UserBase):
    id: int
    registered_at: datetime
    is_confirmed: bool
    last_login: Optional[datetime] = None

    class Config:
         from_attributes = True

# ----- Gallery -----
class GalleryImageBase(BaseModel):
    title: str
    thumb_url: str
    full_url: str
    alt_text: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None

class GalleryImageCreate(GalleryImageBase):
    pass

class GalleryImage(GalleryImageBase):
    id: int
    upload_date: datetime
    views: int
    likes: int

    class Config:
         from_attributes = True

# ----- Todo -----
class TodoTaskBase(BaseModel):
    task_text: str
    priority: int = 0
    category: Optional[str] = None

class TodoTaskCreate(TodoTaskBase):
    pass

class TodoTaskUpdate(BaseModel):
    task_text: Optional[str] = None
    is_completed: Optional[bool] = None
    priority: Optional[int] = None
    category: Optional[str] = None

class TodoTask(TodoTaskBase):
    id: int
    user_id: Optional[int] = None
    is_completed: bool
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
         from_attributes = True

# ----- Calculator -----
class CalculationBase(BaseModel):
    expression: str
    result: float
    is_error: bool = False

class CalculationCreate(CalculationBase):
    user_id: Optional[int] = None

class Calculation(CalculationBase):
    id: int
    calculated_at: datetime

    class Config:
       from_attributes = True






class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    birth_date: Optional[datetime] = None

class UserCreate(UserBase):
    password: str  # Пароль для хэширования
    
    @field_validator('password')
    def password_min_length(cls, v):
        if len(v) < 6:
            raise ValueError('Пароль должен быть минимум 6 символов')
        return v

class User(UserBase):
    id: int
    registered_at: datetime
    is_confirmed: bool
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True