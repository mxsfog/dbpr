import psycopg2
from dataclasses import dataclass
from contextlib import contextmanager
import logging
from typing import Optional, List, Any

@dataclass
class DatabaseConfig:
    """Конфигурация подключения к базе данных"""
    host: str = "127.0.0.1"
    name: str = "pl_first"
    user: str = "postgres"
    password: str = "1478"

class DatabaseError(Exception):
    """Кастомные ошибки базы данных"""
    pass

@contextmanager
def database_connection(config: DatabaseConfig):
    """Контекстный менеджер для работы с базой данных"""
    conn = None
    try:
        conn = psycopg2.connect(
            host=config.host,
            database=config.name,
            user=config.user,
            password=config.password
        )
        yield conn
    except psycopg2.Error as e:
        logging.error(f"Database connection error: {e}")
        raise DatabaseError(f"Failed to connect to database: {e}")
    finally:
        if conn:
            conn.close()

class DatabaseManager:
    """Менеджер для работы с базой данных"""
    def __init__(self, config: DatabaseConfig):
        self.config = config

    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[tuple]:
        """Выполнение SQL запроса"""
        with database_connection(self.config) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query, params)
                    conn.commit()
                    try:
                        return cursor.fetchall()
                    except psycopg2.ProgrammingError:
                        return []
                except psycopg2.Error as e:
                    conn.rollback()
                    logging.error(f"Query execution error: {e}")
                    raise DatabaseError(f"Query execution failed: {e}")

    def handle_parent_table(self, table: str, column: str, operation: str,
                          old_value: Optional[str] = None,
                          new_value: Optional[str] = None) -> Any:
        """Обработка операций с родительскими таблицами"""
        operations = {
            'INSERT': f"INSERT INTO {table} ({column}) VALUES (%s)",
            'DELETE': f"DELETE FROM {table} WHERE {column} = %s",
            'UPDATE': f"UPDATE {table} SET {column} = %s WHERE {column} = %s",
            'SELECT': f"SELECT {column} FROM {table}" + (" WHERE {column} = %s" if old_value else "")
        }

        query = operations.get(operation)
        if not query:
            raise ValueError(f"Unsupported operation: {operation}")

        params = tuple(filter(None, [new_value, old_value])) if operation == 'UPDATE' else (old_value,) if old_value else None

        try:
            return self.execute_query(query, params)
        except DatabaseError as e:
            logging.error(f"Parent table operation failed: {e}")
            return f"Error: table [{table}] or column [{column}] might not exist"

def init_database(config: DatabaseConfig) -> None:
    """Инициализация базы данных при запуске"""
    manager = DatabaseManager(config)
    try:
        # Проверка подключения
        manager.execute_query("SELECT 1")
        logging.info("Database connection successful")
    except DatabaseError as e:
        logging.error(f"Database initialization failed: {e}")
        raise