# auth.py

import sqlite3
from pathlib import Path
import hashlib
import threading

# Путь к базе (в той же папке, что и auth.py)
DB_PATH = Path(__file__).parent / "app.db"

# SQLite по-умолчанию однопоточный: включаем check_same_thread=False
_conn = None
_conn_lock = threading.Lock()

def get_conn():
    global _conn
    with _conn_lock:
        if _conn is None:
            _conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
            _conn.row_factory = sqlite3.Row
        return _conn

def init_db():
    """
    Создаёт таблицу users, если её ещё нет.
    """
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        role     TEXT NOT NULL
    )
    """)
    conn.commit()

def hash_password(password: str) -> str:
    """SHA-256 хеш пароля."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def create_user(username: str, password: str, role: str = "user"):
    """
    Регистрирует нового пользователя.
    Возвращает (True, message) или (False, error_message).
    """
    if not username or not password:
        return False, "Имя и пароль не могут быть пустыми"

    hashed = hash_password(password)
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users(username, password, role) VALUES (?, ?, ?)",
            (username, hashed, role),
        )
        conn.commit()
        return True, "Пользователь успешно создан"
    except sqlite3.IntegrityError:
        return False, "Пользователь с таким именем уже существует"
    except Exception as e:
        return False, f"Ошибка при создании пользователя: {e}"

def authenticate(username: str, password: str):
    """
    Проверяет логин/пароль.
    Возвращает (True, role) или (False, None).
    """
    if not username or not password:
        return False, None

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT password, role FROM users WHERE username = ?",
        (username,),
    )
    row = cursor.fetchone()
    if row:
        hashed = hash_password(password)
        if row["password"] == hashed:
            return True, row["role"]
    return False, None

def ensure_admin():
    """
    Если в таблице нет пользователя 'admin',
    создаём его с паролем 'admin' и ролью 'admin'.
    """
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE username = ?", ("admin",))
    if cursor.fetchone() is None:
        hashed = hash_password("admin")
        cursor.execute(
            "INSERT INTO users(username, password, role) VALUES (?, ?, ?)",
            ("admin", hashed, "admin"),
        )
        conn.commit()

# Инициализируем БД и админа
init_db()
ensure_admin()
