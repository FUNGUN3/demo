import sys
from datetime import datetime, date, timedelta
from decimal import Decimal

from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, DateTime, Date,
    Text, Numeric, func, ForeignKey, inspect
)
from sqlalchemy.orm import declarative_base, Session, relationship

# Базовый класс для моделей
Base = declarative_base()

# ---------- Модели (таблицы) ----------

class BlogPost(Base):
    __tablename__ = 'blog_posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(150), unique=True, nullable=False)
    content = Column(Text, nullable=False)
    published_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    theme_preference = Column(String(20), default='light')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    birth_date = Column(Date)
    registered_at = Column(DateTime, default=datetime.utcnow)
    is_confirmed = Column(Boolean, default=False)
    last_login = Column(DateTime)


class GalleryImage(Base):
    __tablename__ = 'gallery_images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    thumb_url = Column(String(500), nullable=False)
    full_url = Column(String(500), nullable=False)
    alt_text = Column(String(200))
    description = Column(Text)
    upload_date = Column(DateTime, default=datetime.utcnow)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    category = Column(String(50))


class TodoTask(Base):
    __tablename__ = 'todo_tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True)
    task_text = Column(String(500), nullable=False)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    priority = Column(Integer, default=0) 
    category = Column(String(50))


class Calculation(Base):
    __tablename__ = 'calculations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True)
    expression = Column(Text, nullable=False)
    result = Column(Numeric, nullable=False)
    calculated_at = Column(DateTime, default=datetime.utcnow)
    is_error = Column(Boolean, default=False)


class CalculatorSetting(Base):
    __tablename__ = 'calculator_settings'

    user_id = Column(Integer, primary_key=True)
    decimal_places = Column(Integer, default=2)
    theme = Column(String(20), default='light')


#  Создание базы и сессии 
engine = create_engine('sqlite:///blog_landing.db', echo=False)
Base.metadata.drop_all(engine)  
Base.metadata.create_all(engine)
session = Session(engine)


# Заполнение даннымы

def populate_data():
    # Задание 1 посты блога
    posts = [
        BlogPost(
            title="Введение в SQLAlchemy",
            slug="intro-to-sqlalchemy",
            content="Руководство по SQLAlchemy",
            published_at=datetime(2025, 1, 15, 10, 0),
            is_active=True,
            views_count=120,
            likes_count=8,
            theme_preference="dark"
        ),
        BlogPost(
            title="Чей Тайвань?",
            slug="angular-reactive-forms",
            content="Давайте разберемся, чей Тайвань.",
            published_at=datetime(2025, 2, 10, 14, 30),
            is_active=True,
            views_count=85,
            likes_count=5,
            theme_preference="light"
        ),
        BlogPost(
            title="На что хватит 7 минут?",
            slug="css-grid-tips",
            content="Давайте разберемся, на что хватит 7 минут? Например, на похавать что дают",
            published_at=datetime(2025, 3, 5, 9, 15),
            is_active=True,
            views_count=210,
            likes_count=15,
            theme_preference="system"
        ),
        BlogPost(
            title="5 неочевидных мест для отдыха в Подмосковье этим летом",
            slug="typescript-advanced-types",
            content="Лето уже близко, а планы на выходные всё ещё туманны",
            published_at=datetime(2025, 3, 20, 16, 45),
            is_active=False,
            views_count=45,
            likes_count=2,
            theme_preference="dark"
        ),
        BlogPost(
            title="Python FastAPI за 30 минут",
            slug="fastapi-crash-course",
            content="Создаём REST API с автоматической документацией...",
            published_at=datetime(2025, 4, 1, 11, 0),
            is_active=True,
            views_count=305,
            likes_count=22,
            theme_preference="light"
        ),
        BlogPost(
            title="Archi Linux руководства",
            slug="docker-for-frontend",
            content="Начнем с того, что я гей фурри. Меня зовут Петр и это моя история.",
            published_at=datetime(2025, 4, 5, 8, 20),
            is_active=True,
            views_count=67,
            likes_count=4,
            theme_preference="system"
        ),
        BlogPost(
            title="Мифы о здоровом питании: проверьте, что из этого правда",
            slug="testing-react-jest",
            content="«Углеводы — зло», «фрукты нельзя есть после 16:00», «органические продукты всегда полезнее» — слышали такое?",
            published_at=datetime(2025, 4, 8, 13, 10),
            is_active=True,
            views_count=142,
            likes_count=9,
            theme_preference="light"
        ),
    ]
    session.add_all(posts)

    # Задание 2 пользователи
    users = [
        User(
            email="admin@example.com",
            password_hash="hashed_password_123",
            full_name="Администратор Системы",
            birth_date=date(1990, 5, 20),
            registered_at=datetime(2025, 1, 10),
            is_confirmed=True,
            last_login=datetime(2025, 4, 1, 9, 15)
        ),
        User(
            email="test@example.com",
            password_hash="hashed_password_123",
            full_name="Тестовый Пользователь",
            birth_date=date(2005, 8, 12),  # 19 лет (меньше 18 нет, 19 > 18)
            registered_at=datetime(2025, 2, 15),
            is_confirmed=False,
            last_login=None
        ),
        User(
            email="young@example.com",
            password_hash="hashed_password_123",
            full_name="Молодой Посетитель",
            birth_date=date(2010, 3, 3),   # 15 лет
            registered_at=datetime(2025, 3, 20),
            is_confirmed=True,
            last_login=datetime(2025, 4, 5, 18, 30)
        ),
        User(
            email="Timofey@gmail.com",
            password_hash="hashed_password_231312",
            full_name="Тимофей Поляков",
            birth_date=date(1985, 11, 23),
            registered_at=datetime(2025, 3, 25),
            is_confirmed=True,
            last_login=datetime(2025, 4, 8, 10, 5)
        ),
        User(
            email="Aleksandr@mail.ru",
            password_hash="hashed_password_231321",
            full_name="Александр Ермоляев",
            birth_date=date(2007, 7, 19),  # 17 лет
            registered_at=datetime(2025, 4, 1),
            is_confirmed=False,
            last_login=None
        ),
    ]
    session.add_all(users)

    # Задание 3 изображения галереи
    images = [
        GalleryImage(
            title="Закат на озере",
            thumb_url="https://picsum.photos/id/1015/200/150",
            full_url="https://picsum.photos/id/1015/800/600",
            alt_text="Горы и озеро на закате",
            description="Красивый горный пейзаж с отражением в воде.",
            upload_date=datetime(2025, 1, 5),
            views=340,
            likes=28,
            category="пейзаж"
        ),
        GalleryImage(
            title="Лесная тропа",
            thumb_url="https://picsum.photos/id/1043/200/150",
            full_url="https://picsum.photos/id/1043/800/600",
            alt_text="Тропинка в лесу",
            description="Уединённая тропа в сосновом бору.",
            upload_date=datetime(2025, 2, 10),
            views=210,
            likes=17,
            category="пейзаж"
        ),
        GalleryImage(
            title="Городской трафик",
            thumb_url="https://picsum.photos/id/1047/200/150",
            full_url="https://picsum.photos/id/1047/800/600",
            alt_text="Ночной город",
            description="Огни мегаполиса в движении.",
            upload_date=datetime(2025, 2, 28),
            views=560,
            likes=42,
            category="город"
        ),
        GalleryImage(
            title="Кофе и круассан",
            thumb_url="https://picsum.photos/id/1080/200/150",
            full_url="https://picsum.photos/id/1080/800/600",
            alt_text="Завтрак",
            description="Идеальное утро: кофе и выпечка.",
            upload_date=datetime(2025, 3, 15),
            views=185,
            likes=23,
            category="еда"
        ),
        GalleryImage(
            title="Щенок лабрадора",
            thumb_url="https://picsum.photos/id/1025/200/150",
            full_url="https://picsum.photos/id/1025/800/600",
            alt_text="Милый щенок",
            description="Маленький лабрадор с игрушкой.",
            upload_date=datetime(2025, 3, 20),
            views=920,
            likes=76,
            category="животные"
        ),
        GalleryImage(
            title="Цветущая сакура",
            thumb_url="https://picsum.photos/id/1040/200/150",
            full_url="https://picsum.photos/id/1040/800/600",
            alt_text="Ветка сакуры",
            description="Нежные розовые цветы на фоне неба.",
            upload_date=datetime(2025, 4, 1),
            views=450,
            likes=31,
            category="пейзаж"
        ),
        GalleryImage(
            title="Абстрактная архитектура",
            thumb_url="https://picsum.photos/id/106/200/150",
            full_url="https://picsum.photos/id/106/800/600",
            alt_text="Современное здание",
            description="Геометрия современного фасада.",
            upload_date=datetime(2025, 4, 5),
            views=125,
            likes=9,
            category="город"
        )
    ]
    session.add_all(images)

    # Задание 4: задачи TODO
    tasks = [
        TodoTask(
            user_id=1,
            task_text="Написать статью о SQLAlchemy",
            is_completed=False,
            created_at=datetime(2025, 4, 1, 9, 0),
            priority=2,
            category="работа"
        ),
        TodoTask(
            user_id=1,
            task_text="Обновить зависимости в проекте",
            is_completed=True,
            created_at=datetime(2025, 4, 2, 10, 15),
            completed_at=datetime(2025, 4, 3, 14, 30),
            priority=1,
            category="работа"
        ),
        TodoTask(
            user_id=2,
            task_text="Купить продукты: молоко, хлеб, яйца",
            is_completed=False,
            created_at=datetime(2025, 4, 4, 8, 20),
            priority=1,
            category="личное"
        ),
        TodoTask(
            user_id=None,
            task_text="Позвонить врачу",
            is_completed=False,
            created_at=datetime(2025, 4, 5, 11, 0),
            priority=2,
            category="здоровье"
        ),
        TodoTask(
            user_id=3,
            task_text="Подготовить презентацию к встрече",
            is_completed=False,
            created_at=datetime(2025, 4, 6, 15, 45),
            priority=2,
            category="работа"
        ),
        TodoTask(
            user_id=1,
            task_text="Прочитать книгу 'Чистый код'",
            is_completed=False,
            created_at=datetime(2025, 4, 7, 20, 0),
            priority=0,
            category="обучение"
        ),
        TodoTask(
            user_id=2,
            task_text="Оплатить счета за интернет",
            is_completed=True,
            created_at=datetime(2025, 4, 2, 9, 0),
            completed_at=datetime(2025, 4, 2, 10, 30),
            priority=1,
            category="личное"
        ),
        TodoTask(
            user_id=3,
            task_text="Сходить в спортзал",
            is_completed=False,
            created_at=datetime(2025, 4, 8, 7, 30),
            priority=1,
            category="здоровье"
        ),
        TodoTask(
            user_id=None,
            task_text="Забронировать билеты на самолёт",
            is_completed=False,
            created_at=datetime(2025, 4, 3, 16, 0),
            priority=2,
            category="личное"
        ),
        TodoTask(
            user_id=4,
            task_text="Изучить новую библиотеку для анимаций",
            is_completed=False,
            created_at=datetime(2025, 4, 8, 13, 20),
            priority=0,
            category="обучение"
        ),
    ]
    session.add_all(tasks)

    # Задание 5: вычисления
    calculations = [
        Calculation(expression="12 + 3 * 4", result=Decimal("24.0"), calculated_at=datetime(2025, 4, 1, 10, 0)),
        Calculation(expression="(25 - 5) / 4", result=Decimal("5.0"), calculated_at=datetime(2025, 4, 2, 11, 30)),
        Calculation(expression="sqrt(16) + 2^3", result=Decimal("12.0"), calculated_at=datetime(2025, 4, 3, 9, 15)),
        Calculation(expression="100 / 0", result=Decimal("0"), is_error=True, calculated_at=datetime(2025, 4, 4, 14, 20)),
        Calculation(expression="3.14159 * 2", result=Decimal("6.28318"), calculated_at=datetime(2025, 4, 5, 16, 45)),
        Calculation(expression="1 / 3", result=Decimal("0.3333333333"), calculated_at=datetime(2025, 4, 6, 12, 10)),
        Calculation(expression="invalid expression", result=Decimal("0"), is_error=True, calculated_at=datetime(2025, 4, 7, 8, 5)),
    ]
    session.add_all(calculations)

    # Настройки калькулятора (опционально)
    settings = [
        CalculatorSetting(user_id=1, decimal_places=3, theme="dark"),
        CalculatorSetting(user_id=2, decimal_places=2, theme="light"),
    ]
    session.add_all(settings)

    session.commit()
    print("Данные успешно добавлены.\n")


# ---------- Выполнение запросов из заданий ----------

def run_queries():
    print("=== ЗАДАНИЕ 1: Landing page блога ===\n")

    # 3. Активные посты, сортировка по дате публикации DESC
    active_posts = session.query(BlogPost).filter(BlogPost.is_active == True)\
                          .order_by(BlogPost.published_at.desc()).all()
    print("3. Активные посты (отсортированы по дате DESC):")
    for p in active_posts:
        print(f"   {p.published_at.date()} - {p.title} (просмотров: {p.views_count})")
    print()

    # 4. Увеличить views_count для поста с id=3
    post_id3 = session.get(BlogPost, 3)
    if post_id3:
        post_id3.views_count += 1
        session.commit()
        print(f"4. Просмотры поста id=3 увеличены. Новое значение: {post_id3.views_count}\n")
    else:
        print("4. Пост с id=3 не найден.\n")

    # 5. Количество постов по theme_preference
    theme_counts = session.query(BlogPost.theme_preference, func.count(BlogPost.id))\
                          .group_by(BlogPost.theme_preference).all()
    print("5. Количество постов по theme_preference:")
    for theme, cnt in theme_counts:
        print(f"   {theme}: {cnt}")
    print("\n" + "="*50 + "\n")


    print("=== ЗАДАНИЕ 2: Форма регистрации ===\n")

    # 3. Проверка email
    email_to_check = 'test@example.com'
    exists = session.query(User).filter(User.email == email_to_check).first() is not None
    print(f"3. Пользователь с email '{email_to_check}' {'существует' if exists else 'не найден'}\n")

    # 4. Пользователи старше 18 лет
    today = date.today()
    adult_users = session.query(User).filter(User.birth_date < today - timedelta(days=18*365)).all()
    print("4. Пользователи старше 18 лет:")
    for u in adult_users:
        age = (today - u.birth_date).days // 365
        print(f"   {u.full_name} ({u.email}), {age} лет")
    print()

    # 5. Обновить last_login для пользователя id=2
    user_id2 = session.get(User, 2)
    if user_id2:
        user_id2.last_login = datetime.utcnow()
        session.commit()
        print(f"5. last_login для пользователя id=2 обновлён: {user_id2.last_login}\n")
    else:
        print("5. Пользователь с id=2 не найден.\n")

    print("="*50 + "\n")


    print("=== ЗАДАНИЕ 3: Галерея изображений ===\n")

    # 3. Изображения категории 'пейзаж', отсортированные по views DESC
    landscapes = session.query(GalleryImage).filter(GalleryImage.category == 'пейзаж')\
                        .order_by(GalleryImage.views.desc()).all()
    print("3. Изображения категории 'пейзаж' (сортировка по просмотрам DESC):")
    for img in landscapes:
        print(f"   {img.title} - {img.views} просмотров")
    print()

    # 4. Увеличить views для изображения id=4
    img4 = session.get(GalleryImage, 4)
    if img4:
        img4.views += 1
        session.commit()
        print(f"4. Просмотры изображения id=4 увеличены. Новое значение: {img4.views}\n")
    else:
        print("4. Изображение с id=4 не найдено.\n")

    # 5. Топ-3 самых просматриваемых изображений
    top3 = session.query(GalleryImage).order_by(GalleryImage.views.desc()).limit(3).all()
    print("5. Топ-3 изображения по просмотрам:")
    for i, img in enumerate(top3, 1):
        print(f"   {i}. {img.title} — {img.views} просмотров")
    print("\n" + "="*50 + "\n")


    print("=== ЗАДАНИЕ 4: Список задач (TODO) ===\n")

    # 3. Незавершённые задачи, сортировка по приоритету DESC, затем по created_at DESC
    incomplete = session.query(TodoTask).filter(TodoTask.is_completed == False)\
                        .order_by(TodoTask.priority.desc(), TodoTask.created_at.desc()).all()
    print("3. Незавершённые задачи (приоритет DESC, дата создания DESC):")
    for t in incomplete:
        priority_label = ["низкий", "средний", "высокий"][t.priority] if t.priority in (0,1,2) else "неизвестно"
        print(f"   [{priority_label}] {t.task_text[:50]}... (создано {t.created_at.date()})")
    print()

    # 4. Отметить задачу id=5 как завершённую
    task5 = session.get(TodoTask, 5)
    if task5:
        task5.is_completed = True
        task5.completed_at = datetime.utcnow()
        session.commit()
        print(f"4. Задача id=5 отмечена завершённой. completed_at = {task5.completed_at}\n")
    else:
        print("4. Задача с id=5 не найдена.\n")

    # 5. Количество задач по category и is_completed
    counts = session.query(TodoTask.category, TodoTask.is_completed, func.count(TodoTask.id))\
                    .group_by(TodoTask.category, TodoTask.is_completed).all()
    print("5. Количество задач по категориям и статусу завершения:")
    for cat, completed, cnt in counts:
        status = "завершено" if completed else "в процессе"
        print(f"   {cat}: {status} — {cnt}")
    print("\n" + "="*50 + "\n")


    print("=== ЗАДАНИЕ 5: Калькулятор (логика + история) ===\n")

    # 3. Создание таблиц выполнено ранее

    # 5. Последние 10 вычислений (отсортированы по calculated_at DESC)
    last10 = session.query(Calculation).order_by(Calculation.calculated_at.desc()).limit(10).all()
    print("5. Последние 10 вычислений:")
    for calc in last10:
        error_flag = " [ОШИБКА]" if calc.is_error else ""
        print(f"   {calc.calculated_at} | {calc.expression} = {calc.result}{error_flag}")
    print()

    # 6. Среднее количество знаков после запятой в result
    # В SQLite нет прямого способа, сделаем через Python, но можно и через func.length(substr(...))
    # Для демонстрации посчитаем среднее по десятичной части вручную.
    all_results = session.query(Calculation.result).filter(Calculation.is_error == False).all()
    decimal_places_list = []
    for (res,) in all_results:
        # Преобразуем Decimal в строку, убираем конечные нули
        str_val = format(res.normalize(), 'f')
        if '.' in str_val:
            decimal_places_list.append(len(str_val.split('.')[1]))
        else:
            decimal_places_list.append(0)
    avg_decimal = sum(decimal_places_list) / len(decimal_places_list) if decimal_places_list else 0
    print(f"6. Среднее количество знаков после запятой в результате: {avg_decimal:.2f}\n")

    # 7. Количество ошибочных вычислений
    error_count = session.query(func.count(Calculation.id)).filter(Calculation.is_error == True).scalar()
    print(f"7. Количество ошибочных вычислений: {error_count}\n")

    print("="*50)


if __name__ == "__main__":
    populate_data()
    run_queries()