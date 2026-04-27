# app/auth.py
import bcrypt

def hash_password(password: str) -> str:
    """
    Хэширует пароль с использованием bcrypt.
    Возвращает хэш в виде строки.
    """
    # Преобразуем пароль в байты
    password_bytes = password.encode('utf-8')
    
    # Генерируем соль и хэшируем
    salt = bcrypt.gensalt(rounds=12)  # 12 раундов - хороший баланс безопасности и скорости
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Возвращаем хэш как строку для хранения в БД
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет соответствие пароля хэшу.
    """
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    
    return bcrypt.checkpw(password_bytes, hashed_bytes)

# Пример использования
if __name__ == "__main__":
    # Тест
    password = "my_secret_password_123"
    hashed = hash_password(password)
    print(f"Пароль: {password}")
    print(f"Хэш: {hashed}")
    print(f"Длина хэша: {len(hashed)} символов")
    print(f"Проверка верного пароля: {verify_password(password, hashed)}")
    print(f"Проверка неверного пароля: {verify_password('wrong_password', hashed)}")