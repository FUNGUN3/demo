from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.routers import blog, users, gallery, todo, calculator

# Создание таблиц (в продакшене используйте Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog & Tools API")

# Подключаем роутеры
app.include_router(blog.router)
app.include_router(users.router)
app.include_router(gallery.router)
app.include_router(todo.router)
app.include_router(calculator.router)

# Обслуживание статических файлов (фронтенд)
app.mount("/", StaticFiles(directory="static", html=True), name="static")